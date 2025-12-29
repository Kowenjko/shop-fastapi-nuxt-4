from sqlalchemy import func, select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from ..models.product import Product
from ..schemas.product import ProductCreate


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Product]:
        stmt = (
            select(Product).options(joinedload(Product.category)).order_by(Product.id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all_paginated(
        self,
        page: int,
        per_page: int,
        with_total: bool = False,
    ) -> tuple[list[Product], bool, bool, Optional[int]]:
        offset = (page - 1) * per_page

        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .order_by(Product.id)
            .limit(per_page + 1)  # +1 для проверки next
            .offset(offset)
        )

        result = await self.session.execute(stmt)
        products = result.scalars().all()

        has_next = len(products) > per_page
        has_previous = page > 1

        total_items: Optional[int] = None
        if with_total:
            total_stmt = select(func.count()).select_from(Product)
            total_items = await self.session.scalar(total_stmt)

        return products[:per_page], has_previous, has_next, total_items

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .filter(Product.id == product_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_category(self, category_id: int) -> List[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .filter_by(id=category_id)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, product_data: ProductCreate) -> Product:
        db_product = Product(**product_data.model_dump())
        self.session.add(db_product)
        await self.session.commit()
        await self.session.refresh(db_product)
        return db_product

    async def get_multiple_by_ids(self, product_ids: List[int]) -> List[Product]:
        stmt = (
            select(Product)
            .options(joinedload(Product.category))
            .filter(Product.id.in_(product_ids))
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
