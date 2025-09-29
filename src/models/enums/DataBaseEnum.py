from enum import Enum

class DataBaseEnum(Enum):
    """
    DataBaseEnum

    Enum for database collection names.
    Helps avoid hardcoding collection strings across the codebase.
    """

    COLLECTION_PROJECT_NAME = "projects"   # Stores project-level information
    COLLECTION_CHUNK_NAME = "chunks"       # Stores processed file chunks
