from typing import Dict, Any
from app.services.dataframe_analysis_service import DataProcessor
import pandas as pd

class PieChartProcessor():
    @staticmethod
    def process(dataFrame: pd.DataFrame, x_axis: str, columns: str, aggregation: str = "none", metric_label: str = "") -> Dict[str, Any]:
        
        if aggregation == "none":
            # Para pie charts, 'none' no tiene sentido. Por defecto, agrupar y sumar
            result = dataFrame.groupby(x_axis)[columns].sum().reset_index()
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
        
        # Limitar categorías para mejor visualización (Top 6 + Otros)
        MAX_CATEGORIES = 6
        
        if len(result) > MAX_CATEGORIES:
            # Ordenar por valores descendentes
            result = result.sort_values(by=columns, ascending=False)
            
            # Tomar las top 6 categorías
            top_categories = result.head(MAX_CATEGORIES)
            
            # Sumar el resto como "Otros"
            others_sum = result.iloc[MAX_CATEGORIES:][columns].sum()
            
            # Crear una fila para "Otros"
            others_row = pd.DataFrame({x_axis: ["Otros"], columns: [others_sum]})
            
            # Combinar
            result = pd.concat([top_categories, others_row], ignore_index=True)
        
        # Calcular porcentajes para gráficos de pastel
        values = result[columns].tolist()
        total = sum(values)
        percentages = [round((value / total * 100), 2) if total > 0 else 0 for value in values]
        
        return {
            "labels": DataProcessor._convert_to_serializable(result[x_axis].tolist()),
            "data": DataProcessor._convert_to_serializable(percentages)
        }