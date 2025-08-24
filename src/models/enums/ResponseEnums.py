# Response Enumerations: Fixed list of possible responses
from enum import Enum

class ResponseSignal(Enum):

    FILE_VALIDATED_SUCCESS = "File has been validated successfully"
    FILE_INVALID_TYPE = "File type is not supported"
    FILE_TOO_LARGE = "File size is too large"
    FILE_UPLOAD_SUCCESS = "File uploaded successfully"
    FILE_UPLOAD_FAILED = "File upload failed"
