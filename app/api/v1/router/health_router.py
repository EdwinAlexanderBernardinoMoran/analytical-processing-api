from fastapi import APIRouter

health_router = APIRouter(prefix="/health", tags=["Health"])

@health_router.get("")
async def health_check():
    return {
        "status": "alive",
        "message": "Backend is running"
    }
