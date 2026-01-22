from typing import Dict, List, Any
from app.services.dataframe_analysis_service import DataProcessor
import pandas as pd


class LineChartProcessor:
    @staticmethod
    def process(dataFrame: pd.DataFrame, x_axis: str, y_columns: List[str]) -> Dict[str, Any]:

        result = dataFrame.sort_values(x_axis)[[x_axis] + y_columns]
        
        data = {
            "labels": DataProcessor._convert_to_serializable(result[x_axis].tolist()),
            "datasets": []
        }
        
        for col in y_columns:
            data["datasets"].append({
                "label": col,
                "data": DataProcessor._convert_to_serializable(result[col].tolist())
            })
        
        return data