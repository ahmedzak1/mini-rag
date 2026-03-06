from .BaseController import BaseController
from models.db_schemas.projects import Project
from models.db_schemas.data_chunk import DataChunk
from typing import List
from stores.llm.LLMEnums import DocumentTypeEnum
import json

class NLPController(BaseController):
    def __init__(self, generation_client, embedding_client, vectordb_client):
        super().__init__()

        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.vectordb_client = vectordb_client

    def create_collection_name(self, project_id: str):
        return f"Collection_{project_id}".strip()
    
    def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id = project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)
    
    def get_vector_db_collection_info(self, project: Project):

        collection_name = self.create_collection_name(project_id = project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default= lambda x: x.__dict__)
        )
    
    def index_into_vectordb(
            self, project: Project, 
            chunks: List[DataChunk],
            chunk_ids: List[int],
            do_reset: bool = False):

        collection_name = self.create_collection_name(project_id = project.project_id)

        texts = [c.chunk_text for c in chunks]
        metadata = [ c.chunk_metadata for c in chunks]
        vector = [
            
            self.embedding_client.embed(text=text, document_type = DocumentTypeEnum.DOCUMENT.value)

            for text in texts
        ]

        _ = self.vectordb_client.create_collection(
            collection_name = collection_name,
            embedding_size = self.embedding_client.embedding_size,
            do_reset = do_reset

        )

        _ = self.vectordb_client.insert_many(
            collection_name = collection_name,
            texts = texts,
            metadata = metadata,
            vector = vector,
            record_ids = chunk_ids
        )

        return True

    def search_vector_db_collection(self, project: Project, text: str, limit: int =5):

        collection_name = self.create_collection_name(project_id = project.project_id)

        vector = self.embedding_client.embed(
            text=text,
            document_type = DocumentTypeEnum.QUERY.value
        )

        if not vector or len(vector) == 0:
            return False

        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )

        if not results:
            return False 
        
        return json.loads(
            json.dumps(results, default= lambda x: x.__dict__)
        )


