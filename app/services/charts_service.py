
from fastapi import HTTPException, status
from typing import Dict, List, Any
import pandas as pd
from app.services.dataframe_analysis_service import DataProcessor
from app.services.chart_processors import pie_processor, line_processor, bar_processor, scatter_processor

class ChartDataProcessor:

    PROCESS = {
        'bar': bar_processor.BarChartProcessor,
        'line': line_processor.LineChartProcessor,
        'pie': pie_processor.PieChartProcessor,
        'scatter': scatter_processor.ScatterChartProcessor
    }
    @staticmethod
    def prepare_chart_data(
        dataFrame: pd.DataFrame,
        chart_type: str,
        x_axis: str,
        y_axis: str | List[str]
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
            
            columns = y_columns if chart_type not in ["pie", "scatter"] else y_columns[0]

            return processor.process(dataFrame, x_axis, columns)

            # if chart_type == "bar":
            #     return ChartDataProcessor._prepare_bar_data(dataFrame, x_axis, y_columns)
            # elif chart_type == "line":
            #     return ChartDataProcessor._prepare_line_data(dataFrame, x_axis, y_columns)
            # elif chart_type == "pie":
            #     return ChartDataProcessor._prepare_pie_data(dataFrame, x_axis, y_columns[0])
            # elif chart_type == "scatter":
            #     return ChartDataProcessor._prepare_scatter_data(dataFrame, x_axis, y_columns[0])
            # else:
            #     raise ValueError(f"Tipo de gráfico no soportado: {chart_type}")
        
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error preparando datos del gráfico : {str(e)}"
            )

    # @staticmethod
    # def _prepare_bar_data(dataFrame: pd.DataFrame, x_axis: str, y_columns: List[str]) -> Dict[str, Any]:
    #     """Prepare data for bar chart - aggregate by category."""
    #     # Agrupar por x_axis y sumar/promediar los valores
    #     result = dataFrame.groupby(x_axis)[y_columns].agg('sum').reset_index()
        
    #     data = {
    #         "labels": DataProcessor._convert_to_serializable(result[x_axis].tolist()),
    #         "datasets": []
    #     }

    #     print("PASO POR AQUI SIN ERROR")
        
    #     for col in y_columns:
    #         data["datasets"].append({
    #             "label": col,
    #             "data": DataProcessor._convert_to_serializable(result[col].tolist())
    #         })
        
    #     return data
    
    # @staticmethod
    # def _prepare_line_data(dataFrame: pd.DataFrame, x_axis: str, y_columns: List[str]) -> Dict[str, Any]:
    #     """Prepare data for line chart - temporal or sequential data."""
    #     # Ordenar por x_axis para mostrar tendencia
    #     result = dataFrame.sort_values(x_axis)[[x_axis] + y_columns]
        
    #     data = {
    #         "labels": DataProcessor._convert_to_serializable(result[x_axis].tolist()),
    #         "datasets": []
    #     }
        
    #     for col in y_columns:
    #         data["datasets"].append({
    #             "label": col,
    #             "data": DataProcessor._convert_to_serializable(result[col].tolist())
    #         })
        
    #     return data
    
    # @staticmethod
    # def _prepare_pie_data(dataFrame: pd.DataFrame, x_axis: str, y_axis: str) -> Dict[str, Any]:
    #     """Prepare data for pie chart - proportions of a total."""
    #     # Agrupar por categoría y sumar
    #     result = dataFrame.groupby(x_axis)[y_axis].sum().reset_index()
        
    #     return {
    #         "labels": DataProcessor._convert_to_serializable(result[x_axis].tolist()),
    #         "data": DataProcessor._convert_to_serializable(result[y_axis].tolist())
    #     }
    
    # @staticmethod
    # def _prepare_scatter_data(dataFrame: pd.DataFrame, x_axis: str, y_axis: str) -> Dict[str, Any]:
        """Prepare data for scatter plot - correlation between two variables."""
        # Filtrar valores no nulos
        clean_df = dataFrame[[x_axis, y_axis]].dropna()
        
        return {
            "data": DataProcessor._convert_to_serializable(
                list(zip(clean_df[x_axis].tolist(), clean_df[y_axis].tolist()))
            ),
            "labels": {
                "x": x_axis,
                "y": y_axis
            }
        }