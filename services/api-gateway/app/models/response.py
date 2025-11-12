"""
Response models following the standard format
"""
from typing import Optional, TypeVar, Generic
from pydantic import BaseModel


T = TypeVar('T')


class PaginationMeta(BaseModel):
    """Pagination metadata"""
    total: int
    limit: int
    page: int
    total_pages: int
    has_next: bool
    has_previous: bool


class ApiResponse(BaseModel, Generic[T]):
    """Standard API response format"""
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    message: str
    meta: Optional[PaginationMeta] = None
