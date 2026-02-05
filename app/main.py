from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.v1.router.file_upload_router import anality
from app.api.v1.router.charts_router import charts
from app.api.v1.router.health_router import health_router
from app.core.middleware import register_middlewares
from app.core.config import FileConfig

load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Analytical Processing API",
        description="API para análisis de datos con sugerencias de visualización basadas en LLM",
        version="1.0.0",
        
        # Configuración para archivos grandes
        max_request_size=FileConfig.MAX_FILE_SIZE_BYTES,
        timeout=300  # 5 minutos para operaciones largas
    )

    register_middlewares(app)

    # Incluir rutas
    app.include_router(health_router)
    app.include_router(anality)
    app.include_router(charts)

    return app

app = create_app()