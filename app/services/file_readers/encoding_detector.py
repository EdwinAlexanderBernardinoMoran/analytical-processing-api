import chardet
from typing import Optional, Dict

class EncodingDetector:
    # Detecta la codificación de archivos de texto
    
    # Codificaciones comunes a probar en orden de prioridad
    FALLBACK_ENCODINGS = [
        'utf-8',
        'latin-1',
        'iso-8859-1',
        'cp1252',
        'windows-1252'
    ]
    
    # Umbral de confianza mínimo para usar la codificación detectada
    CONFIDENCE_THRESHOLD = 0.7

    # Detecta la codificación de un archivo a partir de sus bytes.
    @staticmethod
    def detect(raw_data: bytes) -> Optional[str]:
        if not raw_data:
            return None
            
        result = chardet.detect(raw_data)
        encoding = result.get('encoding')
        confidence = result.get('confidence', 0)
        
        if encoding and confidence > EncodingDetector.CONFIDENCE_THRESHOLD:
            return encoding
            
        return None
    
    @staticmethod
    def get_fallback_encodings() -> list[str]: # Retorna la lista de codificaciones de respaldo a probar
        return EncodingDetector.FALLBACK_ENCODINGS.copy()
