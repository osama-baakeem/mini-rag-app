# Response Enumerations: Fixed list of possible responses
from enum import Enum

class ResponseSignal(Enum):
    """
    ResponseSignal

    Enum representing fixed response messages for file validation,
    upload, and processing operations.
    Using an enum ensures consistent messages across the application.
    """
    
    FILE_VALIDATED_SUCCESS = "File has been validated successfully"
    FILE_INVALID_TYPE = "File type is not supported"
    FILE_TOO_LARGE = "File size is too large"
    FILE_UPLOAD_SUCCESS = "File uploaded successfully"
    FILE_UPLOAD_FAILED = "File upload failed"
    PROCESSING_FAILD = "Processing failed"
    PROCESSING_SUCCESS = "Processing Succeed"
    NO_FILES_ERROR = "Could not find files"
    FILE_ID_ERROR = "No file was found with this id"
