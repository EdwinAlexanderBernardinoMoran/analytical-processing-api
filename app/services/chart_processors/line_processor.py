from typing import Dict, List, Any
from app.services.dataframe_analysis_service import DataProcessor
import pandas as pd


class LineChartProcessor:
    @staticmethod
    def process(dataFrame: pd.DataFrame, x_axis: str, y_columns: List[str], aggregation: str = "none", metric_label: str = "") -> Dict[str, Any]:
        
        if aggregation == "none":
            result = dataFrame.sort_values(x_axis)[[x_axis] + y_columns]
        elif aggregation == "count":
            result = dataFrame.groupby(x_axis)[y_columns].count().reset_index().sort_values(x_axis)
        else:
            # Mapear avg a mean para pandas
            agg_func = "mean" if aggregation == "avg" else aggregation
            result = dataFrame.groupby(x_axis)[y_columns].agg(agg_func).reset_index().sort_values(x_axis)
            # Redondear a enteros cuando es promedio
            if aggregation == "avg":
                for col in y_columns:
                    result[col] = result[col].round().astype(int)
        
        data = {
            "labels": DataProcessor._convert_to_serializable(result[x_axis].tolist()),
            "datasets": []
        }
        
        for col in y_columns:
            label = metric_label if metric_label else col
            data["datasets"].append({
                "label": label,
                "data": DataProcessor._convert_to_serializable(result[col].tolist())
            })
        
        return data