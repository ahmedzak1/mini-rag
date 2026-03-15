from .BaseController import BaseController
from models.db_schemas import Project, DataChunk
from typing import List
from stores.llm.LLMEnums import DocumentTypeEnum
import json

class NLPController(BaseController):
    def __init__(self, generation_client, embedding_client, vectordb_client, template_parser):
        super().__init__()

        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.vectordb_client = vectordb_client
        self.template_parser = template_parser

    def create_collection_name(self, project_id: str):
        return f"Collection_{self.vectordb_client.default_vector_size}_{project_id}".strip()
    
    async def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id = project.id)
        return await self.vectordb_client.delete_collection(collection_name=collection_name)
    
    async def get_vector_db_collection_info(self, project: Project):

        collection_name = self.create_collection_name(project_id = project.id)
        collection_info = await self.vectordb_client.get_collection_info(collection_name=collection_name)

        return json.loads(
            json.dumps(collection_info, default= lambda x: x.__dict__)
        )
    
    async def index_into_vectordb(
            self, project: Project, 
            chunks: List[DataChunk],
            chunk_ids: List[int],
            do_reset: bool = False):

        collection_name = self.create_collection_name(project_id = project.id)

        texts = [c.chunk_text for c in chunks]
        metadata = [ c.chunk_metadata for c in chunks]
        vector = self.embedding_client.embed(text=texts, document_type = DocumentTypeEnum.DOCUMENT.value)

    

        _ = await self.vectordb_client.create_collection(
            collection_name = collection_name,
            embedding_size = self.embedding_client.embedding_size,
            do_reset = do_reset

        )

        _ = await self.vectordb_client.insert_many(
            collection_name = collection_name,
            texts = texts,
            metadata = metadata,
            vector = vector,
            record_ids = chunk_ids
        )

        return True

    async def search_vector_db_collection(self, project: Project, text: str, limit: int =5):

        query_vector = None

        collection_name = self.create_collection_name(project_id = project.id)

        vectors = self.embedding_client.embed(
            text=text,
            document_type = DocumentTypeEnum.QUERY.value
        )

        if not vectors or len(vectors) == 0:
            return False
        
        if isinstance(vectors, list) and len(vectors) > 0:
            query_vector = vectors[0]

        results = await self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=query_vector,
            limit=limit
        )

        if not results:
            return False 
        
        return results
    
    async def answer_rag_question(self, project: Project, query: str, limit: int =5):

        retrieved_docs = await self.search_vector_db_collection(
            project=project,
            text=query,
            limit=limit
        )

        if not retrieved_docs or len(retrieved_docs) == 0:
            return answer, full_prompt, chat_history
        
        system_prompt = self.template_parser.get("rag", "system_prompt")

        documents_prompt = "\n".join([

                self.template_parser.get("rag", "documents_prompt", {
                        "doc_num": idx + 1,
                        "chunk_text": self.generation_client.process_txt(doc["text"])
                    })

                for idx, doc in enumerate(retrieved_docs)
            ]
        )


        footer_prompt = self.template_parser.get("rag", "footer_prompt", {
            "query": query
        })



        chat_history = [
            self.generation_client.construct_prompt(
                prompt = system_prompt,
                role = self.generation_client.enums.SYSTEM.value
            )
        ]

       

        full_prompt = "\n\n".join(
            [documents_prompt, footer_prompt]
        )
        
        answer = self.generation_client.generate_response(
            prompt = full_prompt,
            chat_history = chat_history
        )

        return answer, full_prompt, chat_history
        


