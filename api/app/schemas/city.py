from typing import List
from pydantic import BaseModel, ConfigDict, Field

from .paginate import PaginateBase


class CityBase(BaseModel):
    id: str = Field(..., description="Unique city identifier")
    name: str
    name_en: str | None = None
    city_type: str | None = None
    lat: float | None = None
    lon: float | None = None
    community: str | None = None
    district: str | None = None
    region: str | None = None
    country: str | None = None


class CityCreate(CityBase):
    pass


class CityResponse(CityBase):
    full_name: str
    model_config = ConfigDict(from_attributes=True)


class CityMetaResponse(BaseModel):
    items: List[CityResponse]
    meta: PaginateBase = Field(..., description="Paginate  pages")


class CityAutocomplete(BaseModel):
    id: str
    name: str
    region: str | None
    district: str | None

    model_config = ConfigDict(from_attributes=True)
