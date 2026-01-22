from typing import Dict, Any
from app.services.dataframe_analysis_service import DataProcessor
import pandas as pd

class PieChartProcessor():
    @staticmethod
    def process(dataFrame: pd.DataFrame, x_axis: str, columns: str) -> Dict[str, Any]:

        result = dataFrame.groupby(x_axis)[columns].sum().reset_index()
        
        return {
            "labels": DataProcessor._convert_to_serializable(result[x_axis].tolist()),
            "data": DataProcessor._convert_to_serializable(result[columns].tolist())
        }