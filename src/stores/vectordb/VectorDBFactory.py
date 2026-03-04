from .VectorDBEnums import VectorDBEnums
from .providers import QdrantDB
from controllers.BaseController import BaseController

class VectorDBFactory:
    def __init__(self, config: dict):
        
        self.config = config
        self.base_controller = BaseController()

    def create(self, provider: str):
        db_path = self.base_controller.get_vectordb_path(vectordb_name=self.config.VECTOR_DB_BACKEND)
        if provider == VectorDBEnums.QDRANT.value:
            return QdrantDB(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD
            )    
        return None