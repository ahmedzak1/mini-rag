from .LLMEnums import LLMEnum
from .providers import OPENAIProvider, CoHereProvider, GROQProvider


class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config

    def create(self, provider):
        if provider == LLMEnum.OPENAI.value:
            return OPENAIProvider(
                api_key = self.config.OPENAI_API_KEY,
                base_url = self.config.OPENAI_BASE_URL,
                default_max_input_token = self.config.DEFAULT_MAX_INPUT_TOKENS,
                default_max_output_token = self.config.DEFAULT_MAX_OUTPUT_TOKENS,
                default_temperature = self.config.DEAFULT_TEMPERATURE
            )

        if provider == LLMEnum.COHERE.value:
            return CoHereProvider(
                api_key = self.config.COHERE_API_KEY,
                default_max_input_token = self.config.DEFAULT_MAX_INPUT_TOKENS,
                default_max_output_token = self.config.DEFAULT_MAX_OUTPUT_TOKENS,
                default_temperature = self.config.DEAFULT_TEMPERATURE
            )

        if provider == LLMEnum.GROQ.value:
            return GROQProvider(
                api_key = self.config.GROQ_API_KEY,
                base_url = self.config.GROQ_BASE_URL,
                default_max_input_token = self.config.DEFAULT_MAX_INPUT_TOKENS,
                default_max_output_token = self.config.DEFAULT_MAX_OUTPUT_TOKENS,
                default_temperature = self.config.DEAFULT_TEMPERATURE
            )
        
        return None