import pandas as pd
import uuid

from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class DataFrameStorageService:

    # Almacenamiento temporal de DataFrames en memoria
    _dataframes: Dict[str, Dict[str, Any]] = {}
    _EXPIRATION_MINUTES = 10  # Los DataFrames expiran después de 60 minutos


    @staticmethod
    def store_dataframe(df: pd.DataFrame) -> str:
        df_id = str(uuid.uuid4())

        DataFrameStorageService._dataframes[df_id] = {
            "dataframe": df,
            "timestamp": pd.Timestamp.now()
        }
        
        # Limpiar DataFrames expirados
        DataFrameStorageService._cleanup_expired_dataframes()
        
        return df_id

    def _cleanup_expired_dataframes():
        now = datetime.now()
        expired_ids = [
            df_id for df_id, data in DataFrameStorageService._dataframes.items()
            if now - data["timestamp"] > timedelta(minutes=DataFrameStorageService._EXPIRATION_MINUTES)
        ]
        for df_id in expired_ids:
            del DataFrameStorageService._dataframes[df_id]

    @staticmethod
    def get_dataframe(df_id: str) -> Optional[pd.DataFrame]:
        
        DataFrameStorageService._cleanup_expired_dataframes()
        data = DataFrameStorageService._dataframes.get(df_id)
        return data["dataframe"] if data else None