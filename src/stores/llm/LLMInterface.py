from abc import ABC, abstractmethod

class LLMInterface(ABC):

    @abstractmethod
    def set_generation_model(self, model_id: str):
        pass
    
    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass

    @abstractmethod
    def generate_response(self, prompt: str, chat_history: list=[], max_output_tokens: int = None, temperature: float = None):
        pass

    @abstractmethod
    def embed(self, text: str, document_type: str = None):
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support embeddings."
        )

    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass