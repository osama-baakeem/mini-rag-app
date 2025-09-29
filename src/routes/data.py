from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
import aiofiles
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest


# Use Uvicorn's error logger for consistent logging
logger = logging.getLogger("uvicorn.error")

# Define router for data-related operations
data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"]
)


# ============================================================
# File Upload Endpoint
# ============================================================
@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings)
):
    """
    Upload a file to a project.

    Steps:
    1. Validate file type and size.
    2. Generate a unique file path inside project directory.
    3. Save file asynchronously in chunks.
    4. Return success/failure signal.

    Args:
        project_id (str): Unique project identifier.
        file (UploadFile): File uploaded via multipart form.
        app_settings (Settings): App config, injected by FastAPI.

    Returns:
        JSONResponse: Signal message + file_id if successful.
    """
    # Validate file properties (type, size)
    data_controller = DataController()
    is_valid, result_signal = data_controller.validate_uploaded(file=file)
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": result_signal}
        )

    # Ensure project directory exists
    project_dir_path = ProjectController().get_project_path(project_id=project_id)

    # Generate unique file name and path
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )

    try:
        # Save file in chunks asynchronously to prevent blocking
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_UPLOAD_FAILED.value}
        )

    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id": file_id
        }
    )


# ============================================================
# File Processing Endpoint
# ============================================================
@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, process_request: ProcessRequest):
    """
    Process an uploaded file by splitting its content into chunks.

    Steps:
    1. Load file content using ProcessController.
    2. Split content into chunks (default: 100 chars with 20 overlap).
    3. Return processed chunks with metadata.

    Args:
        project_id (str): Unique project identifier.
        process_request (ProcessRequest): Request body containing:
            - file_id
            - chunk_size
            - chunk_overlap

    Returns:
        list | JSONResponse: List of chunks on success,
                             error signal on failure.
    """
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    chunk_overlap = process_request.chunk_overlap

    process_controller = ProcessController(project_id=project_id)

    logger.info("Fetching file content...")
    file_content = process_controller.get_file_content(file_id=file_id)

    logger.info("Processing file content...")
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    logger.info(f"Got {len(file_chunks)} chunks")

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.PROCESSING_FAILD.value}
        )

    return file_chunks
