import pandas as pd
import io
from typing import Union
from fastapi import HTTPException, status

from .encoding_detector import EncodingDetector

class CSVReader:
    # Lector robusto de archivos CSV. Maneja múltiples codificaciones, separadores y errores de formato.
    
    SEPARATORS = [',', ';', '\t', '|']
    
    # Configuración para lectura de pandas
    PANDAS_CONFIG = {
        'encoding_errors': 'replace',
        'on_bad_lines': 'skip',
        'engine': 'python'
    }
    
    #  Lee un archivo CSV manejando múltiples codificaciones y separadores.
    @staticmethod
    def read(file_path_or_buffer: Union[str, io.BytesIO]) -> pd.DataFrame:

        # Intentar lectura con detección automática
        if isinstance(file_path_or_buffer, io.BytesIO):
            df = CSVReader._read_from_bytes(file_path_or_buffer)
        else:
            df = CSVReader._read_from_path(file_path_or_buffer)
            
        if df is not None:
            return df
            
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pudo leer el archivo CSV. El archivo puede tener un formato no compatible o estar corrupto."
        )
    
    # Lee CSV desde un buffer de bytes
    @staticmethod
    def _read_from_bytes(buffer: io.BytesIO) -> pd.DataFrame:
        buffer.seek(0)
        raw_data = buffer.read()
        buffer.seek(0)
        
        # Intentar con codificación detectada automáticamente
        detected_encoding = EncodingDetector.detect(raw_data)
        if detected_encoding:
            df = CSVReader._try_read_with_encoding(
                io.BytesIO(raw_data),
                detected_encoding
            )
            if df is not None:
                return df
        
        # Intentar con codificaciones de respaldo
        for encoding in EncodingDetector.get_fallback_encodings():
            df = CSVReader._try_read_with_encoding(
                io.BytesIO(raw_data),
                encoding
            )
            if df is not None:
                return df
                
        return None
    
    # Lee CSV desde un path de archivo
    @staticmethod
    def _read_from_path(path: str) -> pd.DataFrame:
        for encoding in EncodingDetector.get_fallback_encodings():
            df = CSVReader._try_read_with_encoding(path, encoding)
            if df is not None:
                return df
        return None
    
    # Intenta leer el CSV con una codificación específica y todos los separadores.
    @staticmethod
    def _try_read_with_encoding(
        file_path_or_buffer: Union[str, io.BytesIO],
        encoding: str
    ) -> pd.DataFrame:
        
        # Normalizar codificaciones especiales
        if encoding and 'UTF-16' in encoding.upper():
            encoding = 'utf-16'
        
        for separator in CSVReader.SEPARATORS:
            try:
                if isinstance(file_path_or_buffer, io.BytesIO):
                    file_path_or_buffer.seek(0)
                
                df = pd.read_csv(
                    file_path_or_buffer,
                    encoding=encoding,
                    sep=separator,
                    **CSVReader.PANDAS_CONFIG
                )
                
                # Validar que el resultado tiene sentido
                if CSVReader._is_valid_dataframe(df):
                    return df
                    
            except Exception:
                continue
                
        return None
    
    # Valida que un DataFrame tenga estructura válida.
    @staticmethod
    def _is_valid_dataframe(df: pd.DataFrame) -> bool:
        return not df.empty and len(df.columns) > 1
