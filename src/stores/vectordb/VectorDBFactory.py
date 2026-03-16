from .VectorDBEnums import VectorDBEnums
from .providers import QdrantDB, PGVectorProvider
from controllers.BaseController import BaseController
from sqlalchemy.orm import sessionmaker

class VectorDBFactory:
    def __init__(self, config: dict, db_client: sessionmaker):
        
        self.config = config
        self.base_controller = BaseController()
        self.db_client = db_client

    def create(self, provider: str):
        qdrant_db_client = self.base_controller.get_vectordb_path(vectordb_name=self.config.VECTOR_DB_BACKEND)
        if provider == VectorDBEnums.QDRANT.value:
            return QdrantDB(
                db_client=qdrant_db_client,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD
            )    
        
        if provider == VectorDBEnums.PGVECTOR.value:
            return PGVectorProvider(
                db_client=self.db_client,
                default_vector_size=self.config.EMBEDDING_MODEL_SIZE,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD
            )

        return None

           
    
