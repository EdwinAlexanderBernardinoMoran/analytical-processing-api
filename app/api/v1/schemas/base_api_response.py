from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    status_code: int
    message: Optional[str] = None
    data: Optional[T] = None
