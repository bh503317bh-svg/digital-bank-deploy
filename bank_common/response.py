from __future__ import annotations

from typing import Any, Generic, Optional, TypeVar
from uuid import uuid4

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "ok"
    data: Optional[T] = None
    request_id: str = Field(default_factory=lambda: uuid4().hex)


def ok(data: Any = None, message: str = "ok") -> dict:
    return ApiResponse(code=0, message=message, data=data).model_dump()


def fail(code: int, message: str, data: Any = None) -> dict:
    return ApiResponse(code=code, message=message, data=data).model_dump()
