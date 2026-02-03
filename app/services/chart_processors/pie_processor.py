from typing import Dict, Any
from app.services.dataframe_analysis_service import DataProcessor
import pandas as pd

class PieChartProcessor():
    @staticmethod
    def process(dataFrame: pd.DataFrame, x_axis: str, columns: str, aggregation: str = "none", metric_label: str = "") -> Dict[str, Any]:
        
        if aggregation == "none":
            result = dataFrame[[x_axis, columns]]
        elif aggregation == "count":
            # Para count, si x_axis == columns, solo necesitamos contar ocurrencias
            if x_axis == columns:
                result = dataFrame[x_axis].value_counts().reset_index()
                result.columns = [x_axis, 'count']
                columns = 'count'  # Usar la columna de conteo
            else:
                result = dataFrame.groupby(x_axis)[columns].count().reset_index()
        else:
            # Mapear avg a mean para pandas
            agg_func = "mean" if aggregation == "avg" else aggregation
            result = dataFrame.groupby(x_axis)[columns].agg(agg_func).reset_index()
            # Redondear a enteros cuando es promedio
            if aggregation == "avg":
                result[columns] = result[columns].round().astype(int)
        
        return {
            "labels": DataProcessor._convert_to_serializable(result[x_axis].tolist()),
            "data": DataProcessor._convert_to_serializable(result[columns].tolist())
        }