from math import ceil
from urllib.parse import urlencode
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException, status

from app.schemas.paginate import PaginateBase

from ..repositories.product_repository import ProductRepository
from ..repositories.category_repository import CategoryRepository
from ..schemas.product import (
    ProductResponse,
    ProductListResponse,
    ProductCreate,
    ProductMetaResponse,
)


class ProductService:
    def __init__(self, session: AsyncSession):
        self.product_repository = ProductRepository(session)
        self.category_repository = CategoryRepository(session)

    async def get_all_products(self) -> ProductListResponse:
        products = await self.product_repository.get_all()

        # Якщо продуктів нема
        if not products:
            return ProductListResponse(products=[], total=0)

        products_response = [ProductResponse.model_validate(prod) for prod in products]

        return ProductListResponse(
            products=products_response, total=len(products_response)
        )

    async def get_products_paginated(
        self,
        base_url: str,
        page: int = 1,
        per_page: int = 10,
    ) -> ProductMetaResponse:

        # COUNT делаем только на первой странице
        with_total = page == 1

        products, has_prev, has_next, total_items = (
            await self.product_repository.get_all_paginated(
                page=page,
                per_page=per_page,
                with_total=with_total,
            )
        )

        total_pages = ceil(total_items / per_page) if total_items is not None else None

        def build_link(page_number: int) -> str:
            query = urlencode({"page": page_number, "per_page": per_page})
            return f"{base_url}?{query}"

        if not products:
            return ProductListResponse(
                products=[],
                total=0,
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

        products_response = [ProductResponse.model_validate(prod) for prod in products]

        return ProductMetaResponse(
            products=products_response,
            total=len(products_response),
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

    async def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = await self.product_repository.get_by_id(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found",
            )

        return ProductResponse.model_validate(product)

    async def get_products_by_category(self, category_id: int) -> ProductListResponse:
        # Перевіряємо чи існує категорія
        category = await self.category_repository.get_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category with id {category_id} not found",
            )

        # Отримуємо продукти
        products = await self.product_repository.get_by_category(category_id)

        products_response = [ProductResponse.model_validate(prod) for prod in products]

        return ProductListResponse(
            products=products_response, total=len(products_response)
        )

    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        # Перевіряємо чи існує категорія
        category = await self.category_repository.get_by_id(product_data.category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with id {product_data.category_id} does not exist",
            )

        # Створюємо продукт
        product = await self.product_repository.create(product_data)

        return ProductResponse.model_validate(product)
