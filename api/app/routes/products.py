from typing import Annotated
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.services.product_service import ProductService
from app.schemas.product import (
    ProductResponse,
    ProductListResponse,
    ProductCreate,
    ProductMetaResponse,
)

from fastapi_cache.decorator import cache
from app.core.config import settings

router = APIRouter(tags=["Products"])


@router.get("/all", response_model=ProductListResponse, status_code=status.HTTP_200_OK)
async def get_products(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    service = ProductService(session)
    return await service.get_all_products()


@router.get(
    "/",
    response_model=ProductMetaResponse,
    status_code=status.HTTP_200_OK,
)
@cache(expire=300, namespace=settings.cache.namespace.products)  # 5 мин
async def get_products_paginated(
    request: Request,
    page: int = 1,
    per_page: int = 15,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = ProductService(session)
    return await service.get_products_paginated(
        base_url=str(
            request.url.remove_query_params("page").remove_query_params("per_page")
        ),
        page=page,
        per_page=per_page,
    )


@router.get(
    "/{product_id}/", response_model=ProductResponse, status_code=status.HTTP_200_OK
)
async def get_product(
    product_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    service = ProductService(session)
    return await service.get_product_by_id(product_id)


@router.get(
    "/category/{category_id}/",
    response_model=ProductListResponse,
    status_code=status.HTTP_200_OK,
)
async def get_products_by_category(
    category_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    service = ProductService(session)
    return await service.get_products_by_category(category_id)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
):
    service = ProductService(session)
    return await service.create_product(product_data)
