from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    """
    ProcessRequest

    Defines the request body schema for the `/process/{project_id}` endpoint.
    Used to configure how an uploaded file should be processed.
    """
    
    file_id: str
    chunk_size: Optional[int] = 100
    chunk_overlap: Optional[int] = 20
    do_reset: Optional[int] = 0







