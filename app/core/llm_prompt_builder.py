import json
from typing import List, Dict, Any

class LLMPromptBuilder:
    
    @staticmethod
    def build_chart_suggestions_prompt(
        column_names: List[str],
        data_types: Dict[str, str],
        statistical_summary: Dict[str, Any]
    ) -> str:
        
        prompt = f"""Actúa como un analista de datos experto, identifica los patrones o relaciones más interesantes en los datos y dame 4 visualizaciones en Gráfico de barras, línea, pie chart.

        Información del Dataset:

        Columnas: {', '.join(column_names)}
        Eres un analista de datos experto. Actúa como tal
        Tipos de datos:
        {json.dumps(data_types, indent=2)}

        Resumen estadístico:
        {json.dumps(statistical_summary, indent=2)}

        Debes devolver un JSON con el siguiente formato:
        {{
        "charts": [
            {{
            "title": "Título descriptivo del gráfico",
            "chart_type": "bar|line|pie|scatter",
            "parameters": {{
                "x_axis": "nombre_columna",
                "y_axis": "nombre_columna" o ["columna1", "columna2"]
            }},
            "insight": "Análisis breve y detallado sobre qué revela este gráfico"
            }}
        ]
        }}

        Asegúrate de que los tipos de gráfico sean apropiados para los datos:
        - bar: Para comparar categorías
        - line: Para mostrar tendencias temporales o secuenciales
        - pie: Para mostrar proporciones de un total (solo con datos categóricos)
        - scatter: Para mostrar correlaciones entre dos variables numéricas

        VALIDACIÓN FINAL:
        - Verifica que cada x_axis y y_axis exista en la lista de columnas
        - NO agregues texto descriptivo entre paréntesis a los nombres
        - Si hay columnas de fecha, úsalas tal cual están nombradas

        Responde ÚNICAMENTE con el JSON, sin explicaciones adicionales."""

        return prompt