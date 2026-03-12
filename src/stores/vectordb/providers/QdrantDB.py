from qdrant_client import QdrantClient, models
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
from typing import List
import logging
from models.db_schemas import RetrievedDocuments

class QdrantDB(VectorDBInterface):
    def __init__(self, db_path: str, distance_method: str):

        self.client = None
        self.db_path = db_path
        self.distance_method = None

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method == models.Distance.DOT

        self.logger = logging.getLogger(__name__)

    def connect(self):
        self.client = QdrantClient(
            path = self.db_path
        )

    def disconnect(self):
        self.client = None

    def is_collection_exists(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self) -> List:
        return self.client.get_collections()
    
    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name: str):

        if self.is_collection_exists(collection_name):
            return self.client.delete_collection(collection_name=collection_name)
    
    def create_collection(self, collection_name: str, embedding_size: int, do_reset: bool = False):
        
        if do_reset:
            _= self.delete_collection(collection_name=collection_name)

        if not self.is_collection_exists(collection_name=collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config= models.VectorParams(
                    size = embedding_size,
                    distance= self.distance_method
                )
            )

            return True
    
        return False

    def insert_one(self, collection_name: str, text: str, vector: list,
                    metadata: dict = None,
                    record_id: str = None):
        
        if not self.is_collection_exists(collection_name=collection_name):

            self.logger.error(f"Faild to insert record, Collection {collection_name} does not exist")
            return False
        
        try:
        
            _ = self.client.upsert(
                collection_name = collection_name,
                points = [
                    models.PointStruct(
                        id = [record_id],
                        vector=vector,
                        payload = {
                            "text": text, "metadata": metadata
                        }
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"Error while inserting record: {e}")
            return False
        
        return True
        

    def insert_many(self, collection_name: str, texts: list, vector: list,
                     metadata: list = None, record_ids: list = None,
                    batch_size: int = 50):
        
        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range(0, len(texts)))

        for i in range(0, len(texts), batch_size):

            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vector = vector[i:batch_end]
            batch_metadata = metadata[i:batch_end] 
            batch_record_ids = record_ids[i:batch_end]

            batch_points= [

                models.PointStruct(
                    id = batch_record_ids[idx],
                    vector=batch_vector[idx],
                    payload = {
                        "text": batch_texts[idx], "metadata": batch_metadata[idx]
                    }
                )

                for idx in range(len(batch_texts))

            ]

            try:
                _ = self.client.upsert(
                    collection_name=collection_name,
                    points=batch_points
                )
            except Exception as e:
                self.logger.error(f"Error while inserting batch: {e}")
                return False

        return True
    
    def search_by_vector(self, collection_name: str, vector: list, limit: int = 5):

       results= self.client.query_points(
            collection_name=collection_name,
            query=vector,
            limit=limit
        )
       
       if not results:
           return None
       
       return [
            RetrievedDocuments(
                score=point.score,
                text=point.payload["text"]
            ).model_dump()
    for point in results.points
]

