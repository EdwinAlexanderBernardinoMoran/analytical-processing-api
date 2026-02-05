from fastapi import HTTPException, status
import pandas as pd
import numpy as np
import logging
from app.core.config import FileConfig

logger = logging.getLogger(__name__)

class FileValidationService:
    
    # Optimiza el uso de memoria del DataFrame usando downcast de pandas.
    @staticmethod
    def optimize_dataframe_memory(df: pd.DataFrame) -> pd.DataFrame:
        for col in df.columns:
            col_dtype = df[col].dtype
            
            # Optimizar enteros usando downcast nativo de pandas
            if pd.api.types.is_integer_dtype(col_dtype):
                df[col] = pd.to_numeric(df[col], downcast="integer")
            
            # Optimizar floats usando downcast nativo de pandas
            elif pd.api.types.is_float_dtype(col_dtype):
                df[col] = pd.to_numeric(df[col], downcast="float")
            
            # Convertir columnas de texto con pocos valores únicos a category
            elif pd.api.types.is_object_dtype(col_dtype):
                num_unique = df[col].nunique(dropna=True)
                
                # Solo convertir si tiene valores y no más de 1000 únicos
                if num_unique > 0 and num_unique <= 1000:
                    df[col] = df[col].astype("category")
        
        return df
    
    # Valida estructura y contenido del DataFrame, luego optimiza memoria.
    @staticmethod
    def validate_dataframe(dataFrame: pd.DataFrame, min_rows: int = 2) -> pd.DataFrame:
        
        # Validación 1: DataFrame vacío
        if dataFrame.empty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo no contiene datos. Por favor sube un archivo con información válida."
            )
        
        # Validación 2: Sin columnas
        if dataFrame.shape[1] == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo no tiene columnas. Verifica que el formato sea correcto."
            )
        
        # Validación 3: Muy pocas filas
        if len(dataFrame) < min_rows:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El archivo tiene muy pocas filas ({len(dataFrame)}). "
                       f"Se requieren al menos {min_rows} filas para generar análisis."
            )
        
        # Validación 4: Todas las celdas vacías (optimizado con short-circuit)
        if not dataFrame.notna().any().any():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo solo contiene valores vacíos. Por favor sube un archivo con datos válidos."
            )
        
        # Optimización de memoria (best-effort, no falla si hay problemas)
        try:
            dataFrame = FileValidationService.optimize_dataframe_memory(dataFrame)
        except Exception as e:
            logger.warning(f"Memory optimization skipped: {e}")
        
        # Validación 5: Uso de memoria tras optimización
        memory_usage_mb = dataFrame.memory_usage(deep=True).sum() / (1024 * 1024)
        if memory_usage_mb > FileConfig.MAX_DATAFRAME_MEMORY_MB:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=(
                    f"El DataFrame ocupa demasiada memoria ({memory_usage_mb:.2f}MB). "
                    "Intente con un archivo más pequeño o con menos columnas."
                )
            )
        
        return dataFrame
