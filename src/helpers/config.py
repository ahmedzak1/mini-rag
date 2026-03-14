from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int

    FILE_DEFAULT_CHUNK_SIZE: int

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_MAIN_DATABASE: str
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEND: str

    OPENAI_API_KEY: str = None
    OPENAI_BASE_URL: str = None
    
    COHERE_API_KEY: str = None

    GROQ_API_KEY: str = None
    GROQ_BASE_URL: str = None

    GENERATION_MODEL_ID_LITRAL: List[str] = None
    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None

    DEFAULT_MAX_INPUT_TOKENS: int = None
    DEFAULT_MAX_OUTPUT_TOKENS: int = None
    DEAFULT_TEMPERATURE: float = None

    VECTOR_DB_BACKEND_LITRAL= List[str] = None
    VECTOR_DB_BACKEND: str
    VECTOR_DB_PATH: str
    VECTOR_DB_DISTANCE_METHOD: str = None
    VECTOR_DB_PGVEC_INDEX_THRESHOLD: int = 100


    MAIN_LANG: str = "en"
    DEFAULT_LANG: str = "en"


    class Config:
        env_file = ".env"

def get_settings():
    return Settings()