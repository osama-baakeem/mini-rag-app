from .BaseDataModel import BaseDataModel
from .db_schema import Project
from .enum.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    # responsible for the collection name project
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTIOM_PROJECT_NAME.value]




        