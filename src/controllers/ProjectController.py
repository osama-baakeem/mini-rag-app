from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
import os


class ProjectController(BaseController):
    """
    ProjectController

    Extends BaseController to manage project-specific directories.
    Ensures each project has a dedicated storage path under `assets/files/`.
    """

    def __init__(self):
        """
        Initialize ProjectController:
        - Inherit BaseController settings and directory paths
        """
        super().__init__()
    
    def get_project_path(self, project_id: str) -> str:
        """
        Get (or create if missing) the directory path for a given project.

        Args:
            project_id (str): Unique identifier for the project.

        Returns:
            str: Absolute path to the project directory.
        """
        # Construct project directory path inside `assets/files/`
        project_dir = os.path.join(self.files_dir, project_id)

        # Create directory if it does not already exist
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        return project_dir
