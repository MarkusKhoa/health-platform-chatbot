from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseHttpReponse(BaseModel):
    status_code: int = Field(description="Status Code", default=200)
    message: str = Field(description="Message", default="success")


class Pagination(BaseModel):
    page: int = Field(description="Page", default=1)
    limit: int = Field(description="Limit", default=10)
    total_pages: int = Field(description="Total Page", default=0)
    total: int = Field(description="Total Item Counts", default=0)


class CommonResponse(BaseHttpReponse, Generic[T]):
    data: T


class CommonPaginationResponse(BaseHttpReponse, Pagination, Generic[T]):
    items: List[T]
