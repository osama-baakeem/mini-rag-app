from enum import Enum

class ProcessingEnum(Enum):
    """
    ProcessingEnum

    Enum for supported file types during processing.
    Used in ProcessController to determine the correct loader.
    """
    
    TXT = ".txt"
    PDF = ".pdf"
