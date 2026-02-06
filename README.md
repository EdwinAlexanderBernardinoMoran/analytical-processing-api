# API de análisis de datos basada en IA

Esta plataforma permite cargar hojas de cálculo, procesarlas automáticamente y obtener sugerencias de visualización generadas por IA, sin necesidad de herramientas de BI complejas.

## 🛠️ Tecnologías

- **Backend**: FastAPI + Python 3.11
- **IA/LLM**: Google Gemini (google-generativeai)
- **Análisis de datos**: Pandas + NumPy
- **Servidor**: Uvicorn
- **Containerización**: Docker + Docker Compose

## 🎯 Decisiones Técnicas

### FastAPI
- Elegido por su alto rendimiento y soporte nativo de async/await
- Documentación automática con OpenAPI/Swagger integrada
- Validación de datos robusta con Pydantic

### Google Gemini
- API gratuita con límites generosos ideal para prototipado y producción
- Excelentes capacidades de comprensión de datos estructurados y contexto

### Pandas + NumPy
- Estándar de la industria para análisis y manipulación de datos en Python
- Ecosistema maduro con amplia documentación y comunidad activa
- Compatibilidad nativa con múltiples formatos (CSV, Excel, JSON)

### Docker + Docker Compose
- Garantiza consistencia entre entornos de desarrollo, testing y producción
- Simplifica el proceso de despliegue y onboarding de nuevos desarrolladores
- Aísla dependencias del sistema host, evitando conflictos
- Facilita escalabilidad horizontal en entornos cloud


## 📋 Requerimientos

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- API Key de [Google AI Studio](https://aistudio.google.com/app/apikey)

## 🚀 Instalación del proyecto

1. **Clonar el proyecto en tu máquina**

```shell
git clone https://github.com/EdwinAlexanderBernardinoMoran/analytical-processing-api
```

2. **Acceder al directorio del proyecto**

```shell
cd analytical-processing-api
```

3. **Configurar el archivo de variables de entorno**

```shell
cp .env.example .env
```

4. **Configurar tu API Key de Google Gemini**

Edita el archivo `.env` y agrega tu API Key:

```env
GEMINI_API_KEY="tu_api_key_aqui"
```

5. **Levantar el proyecto con Docker**

```shell
docker compose up
```

6. Acceder a la url para visualizar probar los enpoints

```shell
http://localhost:8000/
```

## 📚 Documentación de Endpoints

- [Acceder a la siguiente url para probar los enpoints](http://localhost:8000/docs)

### 1. Analizar archivo

**Endpoint:** `POST /v1/api/analyses/file`

**Descripción:** Carga un archivo CSV/Excel y recibe sugerencias de visualización generadas por IA.

**Parámetros:**

- `file`: Archivo (FormData) - Formatos soportados: `.csv`, `.xls`, `.xlsx`

**Respuesta:**

```json
{
  "status_code": 0,
  "message": "string",
  "data": {
    "dataframe_id": "string",
    "chart_suggestions": [
      {
        "title": "string",
        "chart_type": "string",
        "parameters": {
          "x_axis": "string",
          "y_axis": "string",
          "aggregation": "none",
          "metric_label": ""
        },
        "insight": "string"
      }
    ]
  }
}
```

### 2. Obtener datos del gráfico

**Endpoint:** `GET /v1/api/chart/data`

**Descripción:** Obtiene los datos procesados para generar un gráfico específico.

**Query Parameters:**

```json
{
  "dataframe_id": "string",
  "chart_type": "string",
  "x_axis": "string",
  "y_axis": "string",
  "aggregation": "string",
  "metric_label": "string"  
}
```

**Respuesta:**

```json
{
  "status_code": 0,
  "message": "string",
  "data": {
    "chart_type": "string",
    "datasets": {}
  }
}
```

## 🤖 Enfoque para la ingeniería de Prompts para IA

Mi enfoque de ingeniería de prompts se basa en estructurar las instrucciones para que la IA entienda claramente el objetivo, el rol, el contexto y las restricciones, guiándola paso a paso para producir resultados precisos, consistentes y alineados con los datos reales, minimizando ambigüedades y respuestas genéricas.

### Beneficios del Enfoque

✅ **Reducción de errores**: Validación en el prompt evita sugerencias incompatibles  
✅ **Escalabilidad**: Funciona con cualquier estructura de dataset  
✅ **Claridad**: Instrucciones explícitas reducen ambigüedad en respuestas del LLM  
✅ **Mantenibilidad**: Lógica de validación centralizada en `llm_prompt_builder.py`

## 📁 Estructura del Proyecto

```
analytical-processing-api/
├── .dockerignore
├── .env.example                    # Plantilla de variables de entorno
├── .gitignore
├── Dockerfile                      # Configuración del contenedor
├── docker-compose.yml              # Orquestación de servicios
├── requirements.txt                # Dependencias de Python
├── README.md
└── app/
    ├── main.py                     # Punto de entrada de FastAPI
    ├── api/
    │   └── v1/
    │       ├── router/
    │       │   ├── charts_router.py          # Endpoints de gráficos
    │       │   ├── file_upload_router.py     # Endpoint de carga de archivos
    │       │   └── health_router.py          # Endpoint de health check
    │       └── schemas/
    │           ├── analysis_chemas.py        # Schemas de análisis
    │           ├── base_api_response.py      # Schema base de respuestas
    │           └── chart_schema.py           # Schemas de gráficos
    ├── core/
    │   ├── config.py                         # Configuración de la app
    │   ├── llm_prompt_builder.py            # Constructor de prompts para IA
    │   └── middleware.py                     # Middlewares personalizados
    └── services/
        ├── charts_service.py                 # Lógica de procesamiento de gráficos
        ├── dataframe_analysis_service.py     # Análisis estadístico de datos
        ├── dataframe_storage_service.py      # Gestión de DataFrames en memoria
        ├── file_processing_service.py        # Orquestador de procesamiento
        ├── file_validation_service.py        # Validación de archivos
        ├── llm_service.py                    # Integración con Google Gemini
        ├── chart_processors/                 # Patrón Strategy por tipo de gráfico
        │   ├── bar_processor.py              # Procesador de gráficos de barras
        │   ├── line_processor.py             # Procesador de gráficos de líneas
        │   └── pie_processor.py              # Procesador de gráficos circulares
        └── file_readers/                     # Factory Pattern por formato
            ├── csv_reader.py                 # Lector de archivos CSV
            ├── encoding_detector.py          # Detector automático de encoding
            ├── excel_reader.py               # Lector de archivos Excel
            └── file_reader_factory.py        # Factory de lectores
```

## 👤 Autor

**Edwin Alexander Bernardino Moran**

- GitHub: [@EdwinAlexanderBernardinoMoran](https://github.com/EdwinAlexanderBernardinoMoran)
