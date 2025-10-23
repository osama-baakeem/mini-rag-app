from helpers.config import get_settings, Settings
import os
import random
import string


class BaseController:
    """
    BaseController class

    This class provides common functionality that other controllers can inherit.
    It initializes application settings, manages file directories, 
    and includes utility functions like generating random strings.
    """

    def __init__(self):
        """
        Initialize the BaseController:
        - Load application settings using get_settings()
        - Define base directory path of the project
        - Define path to the 'assets/files' directory
        """
        # Load global application settings from helpers/config.py
        self.app_settings = get_settings()

        # Get the root directory of the project (two levels up from this file)
        self.base_dir = os.path.dirname(os.path.dirname(__file__))

        # Construct path to the folder where files are stored (assets/files)
        self.files_dir = os.path.join(
            self.base_dir,
            "assets/files"
        )


        self.database_dir = os.path.join(
            self.base_dir,
            "assests/database"
        )



    def generate_random_string(self, length: int = 12) -> str:
        """
        Generate a random string consisting of lowercase letters and digits.

        Args:
            length (int, optional): Desired length of the string (default = 12).

        Returns:
            str: Randomly generated string.
        """
        # random.choices() picks characters from ascii_lowercase + digits
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))



    def get_database_path(self, db_name: str):

        database_path = os.path.join(
            self.database_dir, db_name
        )
        
        if not os.path.exists(database_path):
            os.makedirs(database_path)
        
        return database_path