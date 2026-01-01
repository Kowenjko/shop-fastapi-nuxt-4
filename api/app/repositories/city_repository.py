from typing import Optional
from sqlalchemy import desc, distinct, func, or_, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from app.models.city import City
from app.schemas.city import CityCreate


class CityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def bulk_insert(self, cities: list[CityCreate]):
        if not cities:
            return

        stmt = insert(City).values([c.model_dump() for c in cities])
        stmt = stmt.on_conflict_do_nothing(index_elements=["id"])
        await self.session.execute(stmt)
        await self.session.commit()

    async def bulk_insert_fast(self, cities: list[CityCreate]):
        """
        Bulk insert с UPSERT (on conflict do nothing), для 40k+ записей.
        """
        if not cities:
            return

        # Преобразуем схемы Pydantic в dict
        values = [c.model_dump() for c in cities]

        stmt = insert(City).values(values)
        stmt = stmt.on_conflict_do_nothing(index_elements=["id"])

        # Одним execute вставляем все записи
        await self.session.execute(stmt)
        await self.session.commit()

    async def bulk_insert_batches(
        self, cities: list[CityCreate], batch_size: int = 5000
    ):
        """
        Вставка больших данных батчами.
        """
        if not cities:
            return

        for i in range(0, len(cities), batch_size):
            batch = cities[i : i + batch_size]
            values = [c.model_dump() for c in batch]

            stmt = insert(City).values(values)
            stmt = stmt.on_conflict_do_nothing(index_elements=["id"])

            await self.session.execute(stmt)
            await self.session.commit()  # коммит после каждого батча
            print(f"✅ Batch {i//batch_size + 1} ({len(batch)} records) inserted")

    async def get_all_paginated(
        self,
        page: int,
        per_page: int,
        q: Optional[str] = None,
        region: Optional[str] = None,
        district: Optional[str] = None,
        with_total: bool = False,
    ) -> tuple[list[City], bool, bool, Optional[int]]:
        offset = (page - 1) * per_page

        stmt = select(City)

        # 🔍 SEARCH (pg_trgm + prefix)
        if q:
            similarity_name = func.similarity(City.name, q)
            similarity_en = func.similarity(City.name_en, q)

            stmt = stmt.where(
                or_(
                    similarity_name > 0.25,
                    similarity_en > 0.25,
                    City.name.ilike(f"{q}%"),
                    City.name_en.ilike(f"{q}%"),
                )
            ).order_by(desc(func.greatest(similarity_name, similarity_en)))

        # 🎯 FILTERS
        if region:
            stmt = stmt.where(City.region == region)

        if district:
            stmt = stmt.where(City.district == district)

        stmt = stmt.limit(per_page + 1).offset(offset)

        result = await self.session.execute(stmt)
        cities = result.scalars().all()

        has_next = len(cities) > per_page
        has_previous = page > 1

        total_items: Optional[int] = None
        if with_total:
            total_stmt = select(func.count()).select_from(City)

            if q:
                total_stmt = total_stmt.where(
                    or_(
                        City.name.ilike(f"%{q}%"),
                        City.name_en.ilike(f"%{q}%"),
                    )
                )

            if region:
                total_stmt = total_stmt.where(City.region == region)

            if district:
                total_stmt = total_stmt.where(City.district == district)

            total_items = await self.session.scalar(total_stmt)

        return cities[:per_page], has_previous, has_next, total_items

    async def get_city_by_id(self, city_id: str) -> City | None:
        stmt = select(City).where(City.id == city_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_regions(self) -> list[str]:
        stmt = (
            select(distinct(City.region))
            .where(City.region.isnot(None))
            .order_by(City.region)
        )
        result = await self.session.execute(stmt)
        return [row[0] for row in result.fetchall()]

    async def get_districts(self, region: str) -> list[str]:
        stmt = select(distinct(City.district)).where(City.district.isnot(None))
        if region:
            stmt = stmt.where(City.region == region)
        stmt = stmt.order_by(City.district)
        result = await self.session.execute(stmt)
        return [row[0] for row in result.fetchall()]

    async def get_communities(self, region: str, district: str):
        stmt = select(distinct(City.community)).where(City.community.isnot(None))

        if region:
            stmt = stmt.where(City.region == region)

        if district:
            stmt = stmt.where(City.district == district)

        stmt = stmt.order_by(City.community)

        result = await self.session.execute(stmt)
        return [row[0] for row in result.fetchall()]
