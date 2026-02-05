"""Configuración: claves API LLM, settings, etc."""
import os
import google.generativeai as genai

class FileConfig:
    
    # Tamaño máximo de archivo: 200MB (para soportar archivos de 150MB con margen)
    MAX_FILE_SIZE_MB = 200
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    
    # Tamaño de chunk para procesamiento (10MB)
    CHUNK_SIZE = 10 * 1024 * 1024
    
    # Formatos soportados
    SUPPORTED_FORMATS = ['.csv', '.xls', '.xlsx']
    
    # Límite de filas para procesamiento en chunks
    CHUNK_ROWS = 50000
    
    # Límite de memoria para DataFrame (1GB después de optimización)
    MAX_DATAFRAME_MEMORY_MB = 1000

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