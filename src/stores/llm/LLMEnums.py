from enum import Enum

class LLMEnum(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    GROQ = "GROQ"
    

class OPENAIEnum(Enum):

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class CoHereEnum(Enum):

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

    DOCUMENT = "search_document"
    QUERY = "search_query"
    
class DocumentTypeEnum(Enum):

    DOCUMENT = "document"
    QUERY = "query"


class GROQEnum(Enum):

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"