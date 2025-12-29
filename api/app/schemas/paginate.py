from pydantic import BaseModel
from typing import Optional


class PaginationLinks(BaseModel):
    current: str
    next: Optional[str]
    prev: Optional[str]


class PaginateBase(BaseModel):
    page: int
    per_page: int

    total_items: Optional[int]
    total_pages: Optional[int]

    previous_page: Optional[int]
    next_page: Optional[int]

    links: PaginationLinks
