from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum


class ProcessController(BaseController):
    """
    ProcessController

    Handles loading, reading, and processing files (TXT, PDF) 
    for a specific project. Uses LangChain loaders and text splitters 
    to prepare documents for further processing (e.g., AI/ML pipelines).
    """

    def __init__(self, project_id: str):
        """
        Initialize ProcessController:
        - Inherit BaseController settings
        - Store project_id
        - Resolve project_path where files are located

        Args:
            project_id (str): Unique identifier for a project.
        """
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str) -> str:
        """
        Extract the file extension from file_id (e.g., '.txt', '.pdf').

        Args:
            file_id (str): File name or identifier.

        Returns:
            str: File extension (including the dot).
        """
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):
        """
        Get the appropriate loader based on file extension.

        Supports:
        - TXT → TextLoader
        - PDF → PyMuPDFLoader

        Args:
            file_id (str): File name or identifier.

        Returns:
            loader instance or None if unsupported type.
        """
        file_ext = self.get_file_extension(file_id=file_id)

        # Full path to the file inside the project directory
        file_path = os.path.join(self.project_path, file_id)

        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")

        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)

        # Unsupported file type
        return None

    def get_file_content(self, file_id: str) -> list:
        """
        Load file content using the appropriate loader.

        Args:
            file_id (str): File identifier.

        Returns:
            list: List of document objects with content + metadata.
        """
        loader = self.get_file_loader(file_id=file_id)
        return loader.load()

    def process_file_content(self, file_content: list, file_id: str,
                             chunk_size: int = 100, chunk_overlap: int = 20):
        """
        Split file content into smaller text chunks for processing.

        Args:
            file_content (list): List of document objects from loader.
            file_id (str): File identifier.
            chunk_size (int, optional): Max characters per chunk. Default = 100.
            chunk_overlap (int, optional): Overlap between chunks. Default = 20.

        Returns:
            list: List of chunked document objects with text + metadata.
        """
        # Initialize text splitter for chunking content
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,  # Use Python's built-in len for token length
        )

        # Extract plain text from documents
        file_content_text = [rec.page_content for rec in file_content]

        # Extract metadata (page number, source, etc.)
        file_content_metadata = [rec.metadata for rec in file_content]

        # Split content into chunks with metadata preserved
        chunks = text_splitter.create_documents(
            file_content_text,
            metadatas=file_content_metadata
        )

        return chunks
