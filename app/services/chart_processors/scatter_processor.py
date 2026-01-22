from typing import Dict, Any
from app.services.dataframe_analysis_service import DataProcessor
import pandas as pd

class ScatterChartProcessor:
    @staticmethod
    def process(dataFrame: pd.DataFrame, x_axis: str, columns: str) -> Dict[str, Any]:
        
        clean_df = dataFrame[[x_axis, columns]].dropna()
        
        return {
            "data": DataProcessor._convert_to_serializable(
                list(zip(clean_df[x_axis].tolist(), clean_df[columns].tolist()))
            ),
            "labels": {
                "x": x_axis,
                "y": columns
            }
        }