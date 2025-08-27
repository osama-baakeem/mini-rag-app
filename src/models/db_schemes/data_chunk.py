# in this collection will take chunks

from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import objectid


class Project(BaseModel):
    _id: Optional[ObjectId]
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0) # gt: greater than
    chunk_project_id: ObjectId

    class config:
        arbitrary_types_allowd = True



