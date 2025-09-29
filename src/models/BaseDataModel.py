from helpers.config import get_settings, Settings

class BaseDataModel:
    """
    BaseDataModel

    Base class for database models.

    Provides:
    - Access to the database client
    - Access to application settings
    """

    def __init__(self, db_client: object):
        """
        Initialize BaseDataModel.

        Args:
            db_client (object): Database client instance (MongoClient).
        """
        # Store database client for use in derived models
        self.db_client = db_client  

        # Load application settings
        self.app_settings = get_settings()
