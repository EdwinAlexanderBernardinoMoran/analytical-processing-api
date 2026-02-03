import json
from typing import List, Dict, Any

class LLMPromptBuilder:
    
    @staticmethod
    def build_chart_suggestions_prompt(
        column_names: List[str],
        data_types: Dict[str, str],
        statistical_summary: Dict[str, Any]
    ) -> str:
        
        prompt = f"""Actúa como un analista de datos experto que identifica los patrones o relaciones más interesantes en los datos y sugiere 3 visualizaciones (gráfico de barras, línea, pie).


        Información del Dataset:

        Columnas: {', '.join(column_names)}
        Eres un analista de datos experto. Actúa como tal

        Tipos de datos:
        {json.dumps(data_types, indent=2)}

        Resumen estadístico:
        {json.dumps(statistical_summary, indent=2)}

        IMPORTANTE - AGREGACIONES Y PROCESAMIENTO:
        - Si necesitas calcular promedios, sumas, conteos u otras agregaciones, debes especificarlo en el parámetro "aggregation"
        - El backend procesará los datos según la agregación especificada
        - NO asumas que los datos ya están agregados
        - Distingue claramente entre datos crudos y métricas calculadas

        Debes devolver un JSON con el siguiente formato:
        {{
        "charts": [
            {{
            "title": "Título descriptivo del gráfico",
            "chart_type": "bar|line|pie",
            "parameters": {{
                "x_axis": "nombre_columna",
                "y_axis": "nombre_columna" o ["columna1", "columna2"],
                "aggregation": "avg|sum|count|min|max|none",
                "metric_label": "Nombre descriptivo de la métrica calculada"
            }},
            "insight": "Análisis breve y detallado sobre qué revela este gráfico"
            }}
        ]
        }}

        REGLAS PARA AGREGACIONES:
        - aggregation: "avg" - Calcula el promedio del y_axis agrupado por x_axis
        - aggregation: "sum" - Calcula la suma del y_axis agrupado por x_axis
        - aggregation: "count" - Cuenta las ocurrencias agrupadas por x_axis
        - aggregation: "min" - Encuentra el valor mínimo del y_axis por grupo de x_axis
        - aggregation: "max" - Encuentra el valor máximo del y_axis por grupo de x_axis
        - aggregation: "none" - Usa los datos tal cual están (raw data)

        Ejemplos prácticos:
        1. Para "Edad Promedio por Marca de Tarjeta": 
           {{"x_axis": "card_brand", "y_axis": "age", "aggregation": "avg", "metric_label": "Edad Promedio"}}
        2. Para "Total de Ventas por Categoría":
           {{"x_axis": "category", "y_axis": "sales", "aggregation": "sum", "metric_label": "Total de Ventas"}}
        3. Para "Cantidad de Clientes por Ciudad":
           {{"x_axis": "city", "y_axis": "customer_id", "aggregation": "count", "metric_label": "Cantidad de Clientes"}}
        4. Para "Distribución de Clientes por Tipo" (PIE CHART):
           {{"x_axis": "customer_type", "y_axis": "customer_id", "aggregation": "count", "metric_label": "Cantidad"}}

        TIPOS DE GRÁFICO - Usa el apropiado:
        - bar: Para comparar categorías con agregaciones (promedios, sumas, conteos)
        - line: Para tendencias temporales o mostrar promedios/totales a lo largo de categorías secuenciales
        - pie: Para proporciones de un total (requiere aggregation: "count" o "sum")

        ⚠️ REGLA CRÍTICA PARA PIE CHARTS:
        - NUNCA uses la misma columna en x_axis y y_axis
        - x_axis: la columna categórica para agrupar (ejemplo: "marca_tarjeta_credito", "sexo", "categoria")
        - y_axis: una columna DIFERENTE para contar o sumar (ejemplo: "customer_id", "transaction_id", cualquier otra columna)
        - aggregation: siempre "count" o "sum"
        
        ❌ MAL: {{"x_axis": "sexo", "y_axis": "sexo", "aggregation": "count"}}
        ✅ BIEN: {{"x_axis": "sexo", "y_axis": "customer_id", "aggregation": "count"}}
        
        ❌ MAL: {{"x_axis": "marca_tarjeta_credito", "y_axis": "marca_tarjeta_credito", "aggregation": "count"}}
        ✅ BIEN: {{"x_axis": "marca_tarjeta_credito", "y_axis": "transaction_id", "aggregation": "count"}}

        REGLA PARA LINE CHARTS:
        - Usa gráficos de línea SOLO cuando el eje X represente una secuencia ordenada
        (tiempo, fechas, periodos, rangos numéricos continuos).
        - NO uses line charts para categorías nominales sin orden natural.
        - Para comparar promedios entre categorías, prefiere bar charts.


        REGLA SOBRE EL LENGUAJE DEL INSIGHT:
        - Los insights deben ser DESCRIPTIVOS, no inferenciales
        - NO utilices términos estadísticos fuertes como:
            "significativo", "estadísticamente significativo", "prueba", "correlación fuerte", "impacto significativo"
        - Usa en su lugar expresiones como:
            "se observa una diferencia", "se aprecia una variación", "sugiere una posible tendencia",
            "permite comparar", "muestra diferencias aparentes"
        - Asume que NO se han realizado pruebas estadísticas inferenciales

        REGLA PARA metric_label:
        - El "metric_label" debe describir la MÉTRICA resultante de forma clara y concisa
        - Para aggregation: "count" → "Cantidad", "Total", "Número de registros"
        - Para aggregation: "avg" → "Promedio de edad", "Edad promedio", "Promedio"
        - Para aggregation: "sum" → "Total de ventas", "Suma de ingresos"
        - Para aggregation: "min" → "Mínimo", "Valor mínimo"
        - Para aggregation: "max" → "Máximo", "Valor máximo"
        - NO uses nombres de columnas crudas como "nombres" o "customer_id"
        - SIEMPRE incluye metric_label en los parameters

        VALIDACIÓN FINAL:
        - Verifica que cada x_axis y y_axis exista en la lista de columnas
        - NO agregues texto descriptivo entre paréntesis a los nombres
        - Si hay columnas de fecha, úsalas tal cual están nombradas
        - SIEMPRE incluye los parámetros "aggregation" y "metric_label" en parameters
        - Si el insight menciona "promedio", "total", "suma" o "conteo", asegúrate de especificar la aggregation correspondiente

        Responde ÚNICAMENTE con el JSON, sin explicaciones adicionales."""

        return prompt