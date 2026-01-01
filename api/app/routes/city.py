from typing import Annotated
from fastapi import APIRouter, Depends, Query, Request, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.services.city_service import CityService
from app.schemas.city import CityMetaResponse, CityResponse


router = APIRouter(tags=["Cities"])


@router.get("/", response_model=CityMetaResponse)
async def get_cities_paginated(
    request: Request,
    page: int = 1,
    per_page: int = 10,
    name: str | None = Query(None, min_length=2),
    region: str | None = None,
    district: str | None = None,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = CityService(session)

    return await service.get_cities_paginated(
        base_url=str(
            request.url.remove_query_params("page").remove_query_params("per_page")
        ),
        page=page,
        per_page=per_page,
        q=name,
        region=region,
        district=district,
    )


@router.get("/{city_id}/", response_model=CityResponse, status_code=status.HTTP_200_OK)
async def get_city(
    city_id: str,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    service = CityService(session)
    return await service.get_city_by_id(city_id)


@router.get("/regions", response_model=list[str])
async def get_regions(session: AsyncSession = Depends(db_helper.session_getter)):
    service = CityService(session)
    return await service.get_city_regions()


@router.get("/districts", response_model=list[str])
async def get_districts(
    region: str | None = None,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = CityService(session)
    return await service.get_city_districts(region)


@router.get("/communities", response_model=list[str])
async def get_communities(
    region: str | None = None,
    district: str | None = None,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = CityService(session)
    return await service.get_city_communities(region=region, district=district)
