from fastapi import UploadFile, HTTPException, status
import pandas as pd
import io
import tempfile
import os
from typing import Optional

from app.core.config import FileConfig
from app.services.file_readers.file_reader_factory import FileReaderFactory

class FileProcessingService:
    
    # Umbral de tamaño para decidir estrategia de lectura (10MB)
    LARGE_FILE_THRESHOLD = 10 * 1024 * 1024
    
    @staticmethod
    async def read_file_to_dataframe(file: UploadFile) -> pd.DataFrame:
        extension = FileProcessingService._validate_and_get_extension(file.filename)
        
        file_size = await FileProcessingService._validate_file_size(file)
        
        if file_size > FileProcessingService.LARGE_FILE_THRESHOLD:
            return await FileProcessingService._read_large_file(file, extension)
        else:
            return await FileProcessingService._read_small_file(file, extension)
    
    #  Valida el formato del archivo y retorna su extensión.
    @staticmethod
    def _validate_and_get_extension(filename: Optional[str]) -> str:
        if not filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del archivo es inválido"
            )
        
        # Buscar extensión soportada
        filename_lower = filename.lower()
        for ext in FileConfig.SUPPORTED_FORMATS:
            if filename_lower.endswith(ext):
                return ext
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Formato de archivo no soportado. Use: {', '.join(FileConfig.SUPPORTED_FORMATS)}"
        )
    
    # Valida el tamaño del archivo sin cargarlo completamente en memoria.
    @staticmethod
    async def _validate_file_size(file: UploadFile) -> int:
        file_size = 0
        chunk_size = 1024 * 1024  # Leer en chunks de 1MB
        
        # Leer archivo por chunks para obtener tamaño total
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            
            file_size += len(chunk)
            
            # Detener si excede el límite
            if file_size > FileConfig.MAX_FILE_SIZE_BYTES:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"El archivo excede el tamaño máximo permitido de {FileConfig.MAX_FILE_SIZE_MB}MB"
                )
        
        # Resetear puntero del archivo al inicio
        await file.seek(0)
        return file_size
    
    # Lee archivos pequeños directamente en memoria. Estrategia óptima para archivos < 10MB.
    @staticmethod
    async def _read_small_file(file: UploadFile, extension: str) -> pd.DataFrame:
        try:
            contents = await file.read()
            buffer = io.BytesIO(contents)
            
            # Usar el factory para obtener el lector apropiado
            dataframe = FileReaderFactory.read(buffer, extension)
            
            return dataframe
            
        except HTTPException:
            # Re-lanzar excepciones HTTP tal cual
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al procesar el archivo: {str(e)}"
            )
    
    # Lee archivos grandes usando archivo temporal. Evita cargar todo el archivo en memoria de una vez.
    @staticmethod
    async def _read_large_file(file: UploadFile, extension: str) -> pd.DataFrame:
        temp_path = None
        
        try:
            # Crear archivo temporal con la extensión correcta
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=extension
            ) as temp_file:
                temp_path = temp_file.name
                
                # Escribir archivo por chunks
                while True:
                    chunk = await file.read(FileConfig.CHUNK_SIZE)
                    if not chunk:
                        break
                    temp_file.write(chunk)
                
                temp_file.flush()
            
            # Leer desde archivo temporal usando el factory
            dataframe = FileReaderFactory.read(temp_path, extension)
            
            return dataframe
            
        except HTTPException:
            raise
        except MemoryError:
            raise HTTPException(
                status_code=status.HTTP_507_INSUFFICIENT_STORAGE,
                detail="El archivo es demasiado grande para procesar. Intente con un archivo más pequeño."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al procesar el archivo: {str(e)}"
            )
        finally:
            # Limpiar archivo temporal
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass  # Ignorar errores al eliminar archivo temporal
        