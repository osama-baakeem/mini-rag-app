# gives schema to the project  
from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import objectid

class Project(BaseModel):
    # schema(shape) of collection of the project
    _id: Optional[ObjectId]
    project_id: str = Field(..., min_length=1)

    @validator('project_id')
    def validate_project_id(cls, value):
        if not isalnum():
            raise ValueError('project_id must be alphanumeric')

        return Value
    
    class config:
        arbitrary_types_allowd = True


