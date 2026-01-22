from typing import Dict, List, Any
import pandas as pd
from app.services.dataframe_analysis_service import DataProcessor


class BarChartProcessor:
    @staticmethod
    def process(dataFrame: pd.DataFrame, x_axis: str, y_columns: List[str]) -> Dict[str, Any]:
       
        result = dataFrame.groupby(x_axis)[y_columns].agg('sum').reset_index()
        
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
        