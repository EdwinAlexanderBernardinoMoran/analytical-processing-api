"""Configuración: claves API LLM, settings, etc."""
import os
import google.generativeai as genai

class LLMConfig:
    
    # Gemini API settings
    MODEL_NAME = 'gemini-2.5-flash'
    TEMPERATURE = 0.7
    RESPONSE_MIME_TYPE = "application/json"
    
    @staticmethod
    def get_api_key() -> str:

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is not set. "
                "Please set it before using the LLM service."
            )
        return api_key
    
    @staticmethod
    def configure_genai() -> genai.GenerativeModel:

        api_key = LLMConfig.get_api_key()
        genai.configure(api_key=api_key)
        return genai.GenerativeModel(LLMConfig.MODEL_NAME)
    
    @staticmethod
    def get_generation_config() -> dict:

        return {
            "temperature": LLMConfig.TEMPERATURE,
            "response_mime_type": LLMConfig.RESPONSE_MIME_TYPE,
        }