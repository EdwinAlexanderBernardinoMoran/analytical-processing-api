
from fastapi import HTTPException, status
from typing import Dict, List, Any
import pandas as pd
from app.services.dataframe_analysis_service import DataProcessor
from app.services.chart_processors import pie_processor, line_processor, bar_processor

class ChartDataProcessor:

    PROCESS = {
        'bar': bar_processor.BarChartProcessor,
        'line': line_processor.LineChartProcessor,
        'pie': pie_processor.PieChartProcessor
    }
    @staticmethod
    def prepare_chart_data(
        dataFrame: pd.DataFrame,
        chart_type: str,
        x_axis: str,
        y_axis: str | List[str],
        aggregation: str = "none",
        metric_label: str = ""
    ) -> Dict[str, Any]:
        try:
            # Asegurar que y_axis sea lista
            y_columns = [y_axis] if isinstance(y_axis, str) else y_axis
            
            all_columns = [x_axis] + y_columns
            missing_cols = [col for col in all_columns if col not in dataFrame.columns]
            if missing_cols:
                raise ValueError(f"Columnas no encontradas: {', '.join(missing_cols)}")
            
            processor = ChartDataProcessor.PROCESS.get(chart_type)
            if not processor:
                raise ValueError(f"Tipo de gráfico no soportado: {chart_type}")
            
            columns = y_columns if chart_type != "pie" else y_columns[0]

            return processor.process(dataFrame, x_axis, columns, aggregation, metric_label)
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error preparando datos del gráfico : {str(e)}"
            )