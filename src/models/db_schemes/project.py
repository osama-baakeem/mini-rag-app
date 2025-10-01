# gives schema to the project  
from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId 

class Project(BaseModel):
    """
    Pydantic schema representing the 'projects' collection in the database.
    Schema (shape) of a project document.

    Fields:
        _id (Optional[ObjectId]): MongoDB unique identifier for the document.
        project_id (str): Unique alphanumeric project identifier, defined in the router.
    """
     
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @validator('project_id')
    def validate_project_id(cls, value):
        """
        Ensure the project_id is alphanumeric.
        """

        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        return value
    
    class Config:
        """
        Pydantic configuration
        """
        arbitrary_types_allowed = True  # Allow ObjectId type


    @classmethod
    def get_indexes(cls):

        return [
            {
                "key": [
                    ("project_id", 1)
                    ],
                "name": "project_id_index_1",
                "unique": True
            }
        ]



