from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
import logging

logger = logging.getLogger(__name__)

class RequestTimeoutMiddleware(BaseHTTPMiddleware):
    """Middleware para logging de requests largos"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        # Log para requests que toman más de 10 segundos
        if process_time > 10:
            logger.warning(
                f"Request lento detectado: {request.method} {request.url.path} "
                f"tomó {process_time:.2f} segundos"
            )
        
        response.headers["X-Process-Time"] = str(process_time)
        return response

def register_middlewares(app: FastAPI):
    # Middleware para requests largos
    app.add_middleware(RequestTimeoutMiddleware)
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )