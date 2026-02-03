from fastapi import HTTPException, status
import pandas as pd


class FileValidationService:
    
    @staticmethod
    def validate_dataframe(dataFrame: pd.DataFrame, min_rows: int = 2):
        # Validación 1: Archivo vacío
        if dataFrame.empty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo no contiene datos. Por favor sube un archivo con información válida."
            )
        
        # Validación 2: Sin columnas
        if len(dataFrame.columns) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo no tiene columnas. Verifica que el formato sea correcto."
            )
        
        # Validación 3: Pocas filas
        if len(dataFrame) < min_rows:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El archivo tiene muy pocas filas ({len(dataFrame)}). Se requieren al menos {min_rows} filas para generar análisis."
            )
        
        # Validación 4: Todas las celdas vacías
        non_null_cells = dataFrame.notna().sum().sum()
        if non_null_cells == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo solo contiene valores vacíos. Por favor sube un archivo con datos válidos."
            )
        
        return True
