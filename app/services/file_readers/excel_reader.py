import pandas as pd
import io
from typing import Union
from fastapi import HTTPException, status

class ExcelReader:
    
    # Motor recomendado para archivos xlsx
    DEFAULT_ENGINE = 'openpyxl'
    
    @staticmethod
    def read(file_path_or_buffer: Union[str, io.BytesIO]) -> pd.DataFrame:
        try:
            df = pd.read_excel(
                file_path_or_buffer,
                engine=ExcelReader.DEFAULT_ENGINE
            )
            
            if df.empty:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El archivo Excel está vacío o no contiene datos válidos."
                )
                
            return df
            
        except pd.errors.EmptyDataError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo Excel está vacío o no contiene datos válidos."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error al leer el archivo Excel: {str(e)}"
            )
