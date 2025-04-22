from typing import TypeVar, Generic, Optional, Any, List
from pydantic import BaseModel


T = TypeVar("T")


class ResponseBase(BaseModel, Generic[T]):
    code: int = 200
    message: str = "success"
    data: Optional[T] = None


class ResponseList(ResponseBase[List[T]], Generic[T]):
    total: int = 0


class ResponseId(ResponseBase[None]):
    id: int 