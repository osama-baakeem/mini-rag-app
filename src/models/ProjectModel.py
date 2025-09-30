from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    """
    Handles all operations for the 'projects' collection in MongoDB.
    Inherits the database client (`db_client`) from BaseDataModel.
    Provides methods to create, retrieve, and list projects.
    """

    def __init__(self, db_client: object):
        """
        Initialize the ProjectModel and set the collection.
        """
        super().__init__(db_client)
        # Assign the MongoDB collection for projects using the enum
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

    async def create_project(self, project: Project):
        """
        Insert a new Project record into the database.

        Args:
            project (Project): Pydantic Project model instance.

        Returns:
            Project: The same project instance with MongoDB `_id` assigned/added.
        """
        # Convert the Pydantic Project model to a dictionary and insert into MongoDB
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))    
        # Assign the MongoDB-generated ObjectId back to the Python project object
        project._id = result.inserted_id
        return project
    
    async def get_project_or_create_one(self, project_id: str):
        """
        Fetch an existing project by project_id or create a new one if not found.

        Args:
            project_id (str): Application-level unique project identifier.

        Returns:
            Project: The existing or newly created Project instance.
        """
        # Try to find a project in the collection using the application-level project_id
        record = await self.collection.find_one({"project_id": project_id})

        if record is None:
            # If not found, create a new Project instance
            project = Project(project_id=project_id)
            # Insert it into the database and get the MongoDB `_id`
            project = await self.create_project(project)
            return project
        
        # If found, return a Pydantic Project object initialized from the MongoDB record
        return Project(**record)
    
    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        """
        Retrieve all projects with pagination.

        Args:
            page (int): Current page number (default 1)
            page_size (int): Number of projects per page (default 10)

        Returns:
            Tuple[List[Project], int]: List of Project objects and total number of pages
        """
        # Count total documents in the 'projects' collection
        total_documents = await self.collection.count_documents({})

        # Calculate total pages based on page_size
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages += 1

        # Query MongoDB for the current page using skip and limit
        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects = []

        # Iterate asynchronously through the cursor and convert documents to Pydantic Project objects
        async for document in cursor:
            projects.append(Project(**document))

        return projects, total_pages
