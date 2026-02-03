# Extraer columnas, tipos, stats del dataframe

import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple

class DataProcessor:

    @staticmethod
    def extract_schema(df: pd.DataFrame) -> Tuple[List[str], Dict[str, str]]:
        column_names = df.columns.tolist()
        data_types = {col: str(dtype) for col, dtype in df.dtypes.items()}
        
        return column_names, data_types

    @staticmethod
    def get_complete_analysis(df: pd.DataFrame) -> Tuple[List[str], Dict[str, str], Dict[str, Any]]:
        column_names, data_types = DataProcessor.extract_schema(df)
        statistical_summary = DataProcessor.get_statistical_summary(df)

        return column_names, data_types, statistical_summary

    @staticmethod
    def get_statistical_summary(df: pd.DataFrame) -> Dict[str, Any]:
        summary = {}
        
        # Get describe() for numeric columns
        numeric_summary = df.describe().to_dict()
        # Convert to serializable format
        numeric_summary = DataProcessor._convert_to_serializable(numeric_summary)
        summary["numeric_summary"] = numeric_summary
        
        # Get info about non-null counts and data types
        info_dict = {
            "shape": {
                "rows": len(df),
                "columns": len(df.columns)
            },
            "columns_info": {}
        }
        
        for col in df.columns:
            col_info = {
                "non_null_count": int(df[col].count()),
                "null_count": int(df[col].isnull().sum()),
                "dtype": str(df[col].dtype)
            }
            
            # Add unique count for categorical-like columns
            if df[col].dtype == 'object' or df[col].dtype.name == 'category':
                col_info["unique_values"] = int(df[col].nunique())
                sample_values = df[col].dropna().head(5).tolist()
                # Convert any non-serializable values
                col_info["sample_values"] = [DataProcessor._convert_to_serializable(val) for val in sample_values]
            # Handle datetime columns
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                col_info["unique_values"] = int(df[col].nunique())
                sample_values = df[col].dropna().head(5).tolist()
                col_info["sample_values"] = [DataProcessor._convert_to_serializable(val) for val in sample_values]
            
            info_dict["columns_info"][col] = col_info
        
        summary["info"] = info_dict
        
        # Convert the entire summary to ensure everything is serializable
        return DataProcessor._convert_to_serializable(summary)
    
    @staticmethod
    def _convert_to_serializable(value):

        # 1. Valores ya serializables
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value

        if isinstance(value, np.generic):  # cubre int, float, bool, etc.
            python_value = value.item()
            return None if isinstance(python_value, float) and np.isnan(python_value) else python_value

        if hasattr(value, "isoformat"):  # datetime.date, datetime.datetime, etc.
            return value.strftime("%Y-%m-%d")
        # 3. Colecciones (listas, tuplas, sets)
        if isinstance(value, dict):
            return {
                key: DataProcessor._convert_to_serializable(item)
                for key, item in value.items()
            }

        if isinstance(value, (list, tuple, set)):
            return [
                DataProcessor._convert_to_serializable(item)
                for item in value
            ]

        # 4. Arrays de numpy → convertir a lista
        if isinstance(value, np.ndarray):
            return [
                DataProcessor._convert_to_serializable(item)
                for item in value.tolist()
            ]

        # 5. Manejo de valores NA de pandas
        try:
            if pd.isna(value):
                return None
        except Exception:
            pass

        # 6. Último recurso → convertir a string
        return str(value)