import json
from typing import List, Dict, Any

class LLMPromptBuilder:
    
    @staticmethod
    def build_chart_suggestions_prompt(
        column_names: List[str],
        data_types: Dict[str, str],
        statistical_summary: Dict[str, Any]
    ) -> str:
        
        prompt = f"""Actúa como un analista de datos experto, identifica los patrones o relaciones más interesantes en los datos y dame 3 visualizaciones en Gráfico de barras, línea, pie que resuman estos hallazgos.

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
        - aggregation: "avg" - Calcula el promedio del y_axis agrupado por x_axis (SOLO para columnas NUMÉRICAS)
        - aggregation: "sum" - Calcula la suma del y_axis agrupado por x_axis (SOLO para columnas NUMÉRICAS)
        - aggregation: "count" - Cuenta las ocurrencias agrupadas por x_axis (funciona con CUALQUIER tipo de columna)
        - aggregation: "min" - Encuentra el valor mínimo del y_axis por grupo de x_axis (SOLO para columnas NUMÉRICAS)
        - aggregation: "max" - Encuentra el valor máximo del y_axis por grupo de x_axis (SOLO para columnas NUMÉRICAS)
        - aggregation: "none" - Usa los datos tal cual están (raw data)
        
        REGLA CRÍTICA SOBRE TIPOS DE DATOS:
        - ANTES de usar "avg", "sum", "min" o "max", VERIFICA que la columna del y_axis sea NUMÉRICA
        - Revisa el campo "Tipos de datos" al inicio del prompt
        - Las columnas de tipo "object" o "string" contienen TEXTO → SOLO puedes usar "count"
        - Las columnas de tipo "int64", "float64", "int32", "float32" son NUMÉRICAS → puedes usar cualquier agregación
        - Si quieres contar registros agrupados por categoría, usa "count" en CUALQUIER columna
        
        Ejemplos según tipos de datos:
        ✅ CORRECTO: age (int64) con aggregation: "avg" → calcula edad promedio
        ✅ CORRECTO: nombre (object) con aggregation: "count" → cuenta registros
        ✅ CORRECTO: transaction_amount (float64) con aggregation: "sum" → suma totales
        ❌ INCORRECTO: nombre (object) con aggregation: "avg" → NO puedes promediar texto
        ❌ INCORRECTO: categoria (object) con aggregation: "sum" → NO puedes sumar texto
        ❌ INCORRECTO: descripcion (object) con aggregation: "min" → NO puedes calcular mínimo de texto

        Ejemplos prácticos:
        1. Para "Edad Promedio por Marca de Tarjeta" (age es int64): 
           {{"x_axis": "card_brand", "y_axis": "age", "aggregation": "avg", "metric_label": "Edad Promedio"}}
        2. Para "Total de Ventas por Categoría" (sales es float64):
           {{"x_axis": "category", "y_axis": "sales", "aggregation": "sum", "metric_label": "Total de Ventas"}}
        3. Para "Cantidad de Clientes por Ciudad" (customer_id puede ser cualquier tipo):
           {{"x_axis": "city", "y_axis": "customer_id", "aggregation": "count", "metric_label": "Cantidad de Clientes"}}
        4. Para "Distribución de Clientes por Tipo" (PIE CHART - customer_id puede ser cualquier tipo):
           {{"x_axis": "customer_type", "y_axis": "customer_id", "aggregation": "count", "metric_label": "Cantidad"}}
        5. Para "Cantidad de Transacciones por Género" (sexo es object, NO numérico):
           {{"x_axis": "sexo", "y_axis": "transaction_id", "aggregation": "count", "metric_label": "Cantidad de Transacciones"}}

        TIPOS DE GRÁFICO - Usa el apropiado:
        
        BAR CHART
        - Usar para comparar magnitudes entre categorías
        - Cada barra representa una categoría DIFERENTE
        - El objetivo es comparar valores, NO proporciones
        - Las categorías del eje X deben ser discretas

        LINE CHART
        - Usar SOLO cuando el eje X represente una secuencia ordenada
        (fechas, tiempo, periodos, rangos numéricos continuos)
        - Ideal para mostrar tendencias
        - NO usar para categorías nominales sin orden natural
        - Para comparar categorías, usar bar chart

        PIE CHART
        - Representa SIEMPRE proporciones de un total (100%)
        - El objetivo es mostrar partes de un todo, NO comparar valores absolutos
        - Requiere aggregation: "count" o "sum"
        - El backend calculará automáticamente los PORCENTAJES de cada categoría

        - ⚠️ IMPORTANTE: El backend limita automáticamente a las TOP 6 categorías más grandes
        - Las categorías restantes se agrupan automáticamente en "Otros"
        - Ideal para columnas con POCAS categorías únicas (género, tipo de cliente, región, etc.)
        - NO usar pie charts para columnas con muchas categorías únicas (ciudades, estados, IDs)
        - Para datos con muchas categorías, preferir BAR CHART horizontal
        - Ideal para mostrar distribuciones y composiciones simples    

        REGLA CRÍTICA PARA PIE CHARTS:
        - NUNCA uses la misma columna en x_axis y y_axis
        - x_axis: la columna categórica para agrupar (ejemplo: "marca_tarjeta_credito", "sexo", "categoria")
        - y_axis: una columna DIFERENTE para contar o sumar (ejemplo: "customer_id", "transaction_id", cualquier otra columna)
        - aggregation: siempre "count" o "sum"
        
        ❌ MAL: {{"x_axis": "sexo", "y_axis": "sexo", "aggregation": "count"}}
        ✅ BIEN: {{"x_axis": "sexo", "y_axis": "customer_id", "aggregation": "count"}}
        
        ❌ MAL: {{"x_axis": "marca_tarjeta_credito", "y_axis": "marca_tarjeta_credito", "aggregation": "count"}}
        ✅ BIEN: {{"x_axis": "marca_tarjeta_credito", "y_axis": "transaction_id", "aggregation": "count"}}


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