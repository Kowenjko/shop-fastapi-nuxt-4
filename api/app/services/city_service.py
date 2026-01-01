from math import ceil
from urllib.parse import urlencode

from fastapi import HTTPException, status
from app.repositories.city_repository import CityRepository
from app.schemas.city import CityCreate, CityMetaResponse, CityResponse
from app.schemas.paginate import PaginateBase
from app.models import City


class CityService:
    def __init__(self, session):
        self.repository = CityRepository(session)

    async def seed_cities_batch(self, cities: list[CityCreate], batch_size: int = 5000):
        await self.repository.bulk_insert_batches(cities, batch_size)

    async def get_cities_paginated(
        self,
        base_url: str,
        page: int = 1,
        per_page: int = 10,
        q: str | None = None,
        region: str | None = None,
        district: str | None = None,
    ) -> CityMetaResponse:

        with_total = page == 1

        cities, has_prev, has_next, total_items = (
            await self.repository.get_all_paginated(
                page=page,
                per_page=per_page,
                q=q,
                region=region,
                district=district,
                with_total=with_total,
            )
        )

        total_pages = ceil(total_items / per_page) if total_items is not None else None

        def build_link(page_number: int) -> str:
            params = {
                "page": page_number,
                "per_page": per_page,
            }
            if q:
                params["q"] = q
            if region:
                params["region"] = region
            if district:
                params["district"] = district

            return f"{base_url}?{urlencode(params)}"

        return CityMetaResponse(
            items=[self._to_city_response(c) for c in cities],
            meta=PaginateBase(
                page=page,
                per_page=per_page,
                total_items=total_items,
                total_pages=total_pages,
                prev_page=page - 1 if has_prev else None,
                next_page=page + 1 if has_next else None,
                links={
                    "current": build_link(page),
                    "next": build_link(page + 1) if has_next else None,
                    "prev": build_link(page - 1) if has_prev else None,
                },
            ),
        )

    async def get_city_by_id(self, city_id: str) -> CityResponse:
        city = await self.repository.get_city_by_id(city_id)
        self._not_city(city, str(city_id))

        return CityResponse.model_validate(city)

    async def get_city_regions(self) -> list[str]:
        return await self.repository.get_regions()

    async def get_city_districts(self, region: str) -> list[str]:
        return await self.repository.get_districts(region)

    async def get_city_communities(self, region: str, district: str) -> list[str]:
        return await self.repository.get_communities(region=region, district=district)

    def _to_city_response(self, city: City) -> CityResponse:

        return CityResponse(
            id=city.id,
            name=city.name,
            name_en=city.name_en,
            city_type=city.city_type,
            lat=city.lat,
            lon=city.lon,
            community=city.community,
            district=city.district,
            region=city.region,
            country=city.country,
            full_name=city.full_name,
        )

    def _not_city(self, city, city_id: str):
        if not city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City with id {city_id} not found",
            )
