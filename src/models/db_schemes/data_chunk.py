# in this collection will take chunks and will give it schema
from pydantic import BaseModel, Field
from typing import Optional
from bson.objectid import ObjectId 

class DataChunk(BaseModel):
    """
    Chunk

    Pydantic schema representing a chunk of a file in the 'chunks' collection.

    Fields:
        _id (Optional[ObjectId]): MongoDB unique identifier for the document.
                                  If you do not provide a value, MongoDB automatically generates a unique _id for every document.
        chunk_text (str): The actual text content of the chunk.
        chunk_metadata (dict): Metadata associated with the chunk (e.g., page number, source).
        chunk_order (int): Order of the chunk in the original file (must be > 0).
        chunk_project_id (ObjectId): Reference to the project this chunk belongs to.
    """

    id: Optional[ObjectId] = Field(default=None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0) # gt: greater than
    chunk_project_id: ObjectId

    class Config:
        """
        Pydantic configuration
        """
        arbitrary_types_allowed = True  # Allow ObjectId type
