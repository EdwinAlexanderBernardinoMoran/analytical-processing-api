import json
from typing import List, Dict, Any

class LLMPromptBuilder:
    
    @staticmethod
    def build_chart_suggestions_prompt(
        column_names: List[str],
        data_types: Dict[str, str],
        statistical_summary: Dict[str, Any]
    ) -> str:
        
        prompt = f"""Actúa como un analista de datos experto. Analiza los datos y genera ÚNICAMENTE visualizaciones que sean COMPATIBLES con la estructura y tipo de datos disponibles.

        Información del Dataset:

        Columnas: {', '.join(column_names)}

        Tipos de datos:
        {json.dumps(data_types, indent=2)}

        Resumen estadístico:
        {json.dumps(statistical_summary, indent=2)}
        
        PASO 1 - ANÁLISIS DE COMPATIBILIDAD (OBLIGATORIO):
        
        Antes de proponer gráficos, DEBES analizar:
        
        1. ¿Hay columnas categóricas? (object, string)
        2. ¿Hay columnas numéricas? (int64, float64, int32, float32)
        3. ¿Hay columnas temporales? (datetime, date)
        4. ¿Cuántas categorías únicas tienen las columnas categóricas?
        5. ¿Existe relación categórica → métrica numérica?
        
        PASO 2 - DETERMINAR GRÁFICOS COMPATIBLES:
        
        ✅ BAR CHART es compatible SI:
        - Existe AL MENOS una columna categórica (para x_axis)
        - Y existe AL MENOS una columna numérica O cualquier columna para contar (para y_axis con aggregation)
        
        ✅ LINE CHART es compatible SI:
        - Existe AL MENOS una columna temporal/secuencial (fechas, periodos) O numérica ordenada (para x_axis)
        - Y existe AL MENOS una columna numérica para el eje Y
        - NO usar para categorías nominales sin orden
        
        ✅ PIE CHART es compatible SI:
        - Existe AL MENOS una columna categórica con POCAS categorías únicas (idealmente ≤ 10)
        - Y existe AL MENOS otra columna diferente para contar o sumar
        - El objetivo es mostrar proporciones de un todo
        
        ⚠️ SI UN TIPO DE GRÁFICO NO ES COMPATIBLE, NO LO PROPONGAS
        
        PASO 3 - GENERAR SOLO GRÁFICOS COMPATIBLES:
        
        - Propón entre 1 y 3 visualizaciones
        - SOLO incluye gráficos que sean compatibles según el análisis anterior
        - NO fuerces un tipo de gráfico si los datos no lo permiten
        - Prioriza los gráficos más reveladores e informativos

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

        EJEMPLOS DE ESCENARIOS Y COMPATIBILIDAD:
        
        ESCENARIO 1: Solo columnas categóricas (nombres, ciudades, categorías)
        ✅ Compatible: BAR CHART (con aggregation: "count")
        ✅ Compatible: PIE CHART (si hay pocas categorías, con aggregation: "count")
        ❌ NO compatible: LINE CHART (no hay secuencia temporal)
        
        ESCENARIO 2: Solo columnas numéricas (precios, cantidades, IDs numéricos)
        ✅ Compatible: LINE CHART (si representan secuencia)
        ✅ Compatible: BAR CHART (comparando valores)
        ❌ Generalmente NO: PIE CHART (a menos que sean categorías discretas limitadas)
        
        ESCENARIO 3: Mix categóricas + numéricas
        ✅ Compatible: BAR CHART (categorías en X, métricas en Y)
        ✅ Compatible: PIE CHART (si las categorías son pocas)
        ❌ NO compatible: LINE CHART (a menos que haya fechas/tiempo)
        
        ESCENARIO 4: Tiene columnas de fecha/tiempo
        ✅ Compatible: LINE CHART (fechas en X, métricas en Y)
        ✅ Compatible: BAR CHART (periodos en X, métricas en Y)
        ❌ Generalmente NO: PIE CHART (fechas no representan partes de un todo)
        
        TIPOS DE GRÁFICO - Especificaciones detalladas:
        
        BAR CHART - Requisitos de compatibilidad:
        ✅ USAR cuando:
        - Comparar magnitudes entre categorías discretas
        - Tienes columnas categóricas (tipos, marcas, regiones)
        - Cada barra representa una categoría DIFERENTE
        - El objetivo es comparar valores, NO proporciones
        ❌ NO USAR cuando:
        - No hay columnas categóricas
        - Solo tienes datos temporales continuos (usar line chart)
        
        LINE CHART - Requisitos de compatibilidad:
        ✅ USAR cuando:
        - El eje X representa una secuencia ORDENADA: fechas, tiempo, periodos, años
        - Ideal para mostrar tendencias temporales o progresión
        - Tienes al menos una columna temporal o numérica secuencial
        ❌ NO USAR cuando:
        - No hay columnas temporales ni secuenciales
        - Solo tienes categorías nominales (género, tipo, marca) → usar bar chart
        - Para comparar categorías discretas → usar bar chart
        
        PIE CHART - Requisitos de compatibilidad:
        ✅ USAR cuando:
        - Quieres mostrar proporciones de un TODO (100%)
        - La columna categórica tiene POCAS categorías (idealmente ≤ 10)
        - Tienes columnas categóricas como: género (2-3 valores), tipo de cliente (3-5 valores), región (5-8 valores)
        - El objetivo es mostrar composición, NO comparar magnitudes
        ❌ NO USAR cuando:
        - La columna tiene MUCHAS categorías únicas (>10-15): ciudades, productos, IDs
        - No hay columnas categóricas
        - Quieres comparar valores absolutos → usar bar chart
        - La columna es temporal (fechas) → usar line chart
        - Para muchas categorías, preferir bar chart horizontal  

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