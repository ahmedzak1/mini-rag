from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int

    FILE_DEFAULT_CHUNK_SIZE: int

    MONGO_URI: str
    MONGO_DB_DATABASE: str

    GENERATION_BACKEND: str
    EMBEDDING_BACKEDND: str

    OPENAI_API_KEY: str = None
    OPENAI_BASE_URL: str = None
    
    COHERE_API_KEY: str = None

    GROQ_API_KEY: str = None
    GROQ_BASE_URL: str = None


    GENERATION_MODEL_ID: str = None
    EMBEDDING_MODEL_ID: str = None
    EMBEDDING_MODEL_SIZE: int = None

    DEFAULT_MAX_INPUT_TOKENS: int = None
    DEFAULT_MAX_OUTPUT_TOKENS: int = None
    DEAFULT_TEMPERATURE: float = None

    class Config:
        env_file = ".env"

def get_settings():
    return Settings()