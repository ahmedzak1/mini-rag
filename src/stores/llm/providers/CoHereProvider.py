from ..LLMInterface import LLMInterface
from .. LLMEnums import CoHereEnum, DocumentTypeEnum
import cohere
import logging


class CoHereProvider(LLMInterface):
    
    def __init__(self, api_key: str, default_max_input_token: int = 1000,
                 default_max_output_token: int = 1000, default_temperature: float = 0.1):

        self.api_key = api_key
        self.default_max_input_token = default_max_input_token
        self.default_max_output_token = default_max_output_token
        self.default_temperature = default_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None 

        self.client = cohere.ClientV2(api_key = self.api_key)
        self.enums = CoHereEnum

        self.logger = logging.getLogger(__name__)


    def set_generation_model(self, model_id: str):

        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):

        self.embedding_model_id = model_id 
        self.embedding_size = embedding_size

    def process_txt(self, text: str):

        return text[:self.default_max_input_token].strip()


    def generate_response(self, prompt: str, chat_history: list=[], max_output_tokens: int = None, temperature: float = None): 

        if not self.client:
            self.logger.error("Failed to initialize cohere client. Client instance is None.")
            return None

        if not self.generation_model_id:
            self.logger.error("Model ID is not configured.")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_max_input_token
        temperature = temperature if temperature else self.default_temperature

        chat_history.append(
            self.construct_prompt(prompt = prompt, role = CoHereEnum.USER.value)
        )

        response = self.client.chat(

            model = self.generation_model_id,
            messages = chat_history,
            temperature = temperature,
            max_tokens= max_output_tokens 
        )    

        if not response or not response.text or not response.message.content[0].text:
            self.logger.error("Invalid or empty chat response.")
            return None 
        
        return response.message.content[0].text


    def embed(self, text: str, document_type: str = None):
        
        if not self.client:
            self.logger.error("Failed to initialize cohere client. Client instance is None.")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not configured.")
            return None
        
        input_type = CoHereEnum.DOCUMENT

        if document_type == DocumentTypeEnum.QUERY:
            input_type = CoHereEnum.QUERY

        response = self.client.embed(
            model = self.embedding_model_id, 
            texts = [self.process_txt(text)],
            input_type= input_type,
            embedding_types=["float"],
        )

        if not response or not response.embeddings or not response.embeddings.float:

            self.logger.error("Error While Embedding Text") 
            return None

        return response.embeddings.float[0]



    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "text": prompt
        }