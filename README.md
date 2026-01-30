# API de análisis de datos basada en IA

Esta plataforma permite cargar hojas de cálculo, procesarlas automáticamente y obtener sugerencias de visualización generadas por IA, sin necesidad de herramientas de BI complejas.

## 🛠️ Tecnologías

- **Backend**: FastAPI + Python 3.11
- **IA/LLM**: Google Gemini (google-generativeai)
- **Análisis de datos**: Pandas + NumPy
- **Servidor**: Uvicorn
- **Containerización**: Docker + Docker Compose

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

### 1. Analizar archivo

**Endpoint:** `POST /v1/api/analyses/file`

**Descripción:** Carga un archivo CSV/Excel y recibe sugerencias de visualización generadas por IA.

**Parámetros:**

- `file`: Archivo (FormData) - Formatos soportados: `.csv`, `.xls`, `.xlsx`

**Respuesta:**

```json
{
  "status_code": 200,
  "message": "Analysis successfully completed",
  "data": {
    "dataframe_id": "uuid-generado",
    "chart_suggestions": [
      {
        "title": "Distribución de ventas por categoría",
        "chart_type": "bar",
        "parameters": {
          "x_axis": "categoria",
          "y_axis": "ventas"
        },
        "insight": "Se observa que la categoría Electrónica representa el 45% de las ventas totales..."
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
  "dataframe_id": "uuid-del-dataframe",
  "chart_type": "bar",
  "x_axis": "categoria",
  "y_axis": "ventas"
}
```

**Respuesta:**

```json
{
  "status_code": 200,
  "message": "Chart data successfully retrieved",
  "data": {
    "chart_type": "bar",
    "datasets": {
      "labels": ["Electrónica", "Ropa", "Alimentos"],
      "data": [45000, 32000, 28000]
    }
  }
}
```

## 📁 Estructura del Proyecto

```
analytical-processing-api/
├── app/
│   ├── main.py                 # Punto de entrada de FastAPI
│   ├── api/
│   │   └── v1/
│   │       ├── router/         # Endpoints
│   │       └── schemas/        # Modelos Pydantic
│   ├── core/
│   │   ├── config.py           # Configuración
│   │   ├── llm_prompt_builder.py  # Prompts para LLM
│   │   └── middleware.py       # Middleware
│   └── services/
│       ├── llm_service.py      # Integración con Gemini
│       ├── dataframe_analysis_service.py
│       ├── charts_service.py
│       └── chart_processors/   # Procesadores por tipo
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## 👤 Autor

**Edwin Alexander Bernardino Moran**

- GitHub: [@EdwinAlexanderBernardinoMoran](https://github.com/EdwinAlexanderBernardinoMoran)
