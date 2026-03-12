from ..LLMInterface import LLMInterface
from .. LLMEnums import GROQEnum
from groq import Groq
import logging


class GROQProvider(LLMInterface):
    
    def __init__(self, api_key: str, base_url: str, default_max_input_token: int = 1000,
                 default_max_output_token: int = 1000, default_temperature: float = 0.1):

        self.api_key = api_key
        self.base_url = base_url
        self.default_max_input_token = default_max_input_token
        self.default_max_output_token = default_max_output_token
        self.default_temperature = default_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None 

        self.client = Groq(  
            api_key=self.api_key,
            base_url= self.base_url
        )

        self.enums = GROQEnum
        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):

        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):

        raise NotImplementedError(
            "GroqProvider does not support embedding models. "
            "Configure EMBEDDING_BACKEND with a provider that supports embeddings."
        )
    
    def process_txt(self, text: str):

        return text[:self.default_max_input_token].strip()
    

    def generate_response(self, prompt: str, chat_history: list=[], max_output_tokens: int = None, temperature: float = None): 

        if not self.client:
            self.logger.error("Failed to initialize Groq client. Client instance is None.")
            return None

        if not self.generation_model_id:
            self.logger.error("Model ID is not configured.")
            return None

        max_output_tokens = max_output_tokens if max_output_tokens else self.default_max_input_token
        temperature = temperature if temperature else self.default_temperature

        chat_history.append(
            self.construct_prompt(prompt = prompt, role = GROQEnum.USER.value)
        )

        response = self.client.chat.completions.create(

            model = self.generation_model_id,
            messages = chat_history,
            max_tokens = max_output_tokens,
            temperature = temperature
        )

        if (
            not response
            or not response.choices
            or len(response.choices) == 0
            or not response.choices[0].message
            or not response.choices[0].message.content
            ):

            self.logger.error("Invalid or empty chat response.")
            return None

        return response.choices[0].message.content
    
    def embed(self, text: str, document_type: str = None):
        raise NotImplementedError(
            "GroqProvider does not support embeddings."
        )

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": prompt
        }

