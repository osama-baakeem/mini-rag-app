from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseSignal
from .ProjectController import ProjectController
import re
import os


class DataController(BaseController):
    """
    DataController

    Extends BaseController to handle file-related operations:
    - Validating uploaded files
    - Generating unique file paths
    - Cleaning file names
    """

    def __init__(self):
        """
        Initialize DataController:
        - Call BaseController to load settings and paths
        - Define size_scale to convert MB → bytes (1 MB = 1048576 bytes)
        """
        super().__init__()
        self.size_scale = 1048576  # Conversion factor: MB → Bytes

    def validate_uploaded(self, file: UploadFile):
        """
        Validate uploaded file based on type and size.

        Args:
            file (UploadFile): Uploaded file object from FastAPI.

        Returns:
            tuple: (bool, str) where
                - bool indicates success or failure,
                - str contains a ResponseSignal value.
        """
        # Check if file type is allowed
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_INVALID_TYPE.value

        # Check if file exceeds maximum size (convert MB → bytes)
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_TOO_LARGE.value

        return True, ResponseSignal.FILE_VALIDATED_SUCCESS.value

    def generate_unique_filepath(self, orig_file_name: str, project_id: str):
        """
        Generate a unique file path for saving uploaded files.

        Args:
            orig_file_name (str): Original uploaded file name.
            project_id (str): Associated project ID.

        Returns:
            tuple: (new_file_path, unique_file_name)
        """
        # Generate random key to ensure uniqueness
        random_key = self.generate_random_string()

        # Get project directory path using ProjectController
        project_path = ProjectController().get_project_path(project_id=project_id)

        # Clean the original file name
        cleaned_file_name = self.get_clean_filename(orig_file_name=orig_file_name)

        # Build full path: project directory + random key + cleaned file name
        new_file_path = os.path.join(
            project_path,
            random_key + "_" + cleaned_file_name
        )

        # Ensure the file name is unique (regenerate if file already exists)
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(
                project_path,
                random_key + "_" + cleaned_file_name
            )

        return new_file_path, random_key + "_" + cleaned_file_name

    def get_clean_filename(self, orig_file_name: str) -> str:
        """
        Clean and sanitize file name.

        - Remove special characters (except underscore `_` and dot `.`)
        - Trim leading/trailing spaces
        - Replace spaces with underscores

        Args:
            orig_file_name (str): Original uploaded file name.

        Returns:
            str: Cleaned file name.
        """
        # Remove unwanted characters
        cleaned_file_name = re.sub(r'[^\w.]', '', orig_file_name.strip())

        # Replace spaces with underscores
        cleaned_file_name = cleaned_file_name.replace(' ', '_')

        return cleaned_file_name
