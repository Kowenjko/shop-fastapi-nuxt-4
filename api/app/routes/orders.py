from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.services.order_service import OrderService
from app.schemas.order import (
    OrderProductsAddSchema,
    OrderReadSchema,
    OrderSummarySchema,
    OrderCreateSchema,
    OrderProductUpdateSchema,
    AddProductRequest,
    UpdateProductRequest,
    RemoveProductRequest,
    CancelOrderRequest,
    CheckoutRequest,
    OrderProductsReplaceSchema,
)

router = APIRouter(tags=["Orders"])


@router.post("/", response_model=OrderReadSchema, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreateSchema,
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    service = OrderService(session)
    return await service.create_order(user_id, data)


@router.get(
    "/{order_id}/",
    response_model=OrderReadSchema,
    status_code=status.HTTP_200_OK,
)
async def get_order(
    order_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    service = OrderService(session)
    return await service.get_order_by_id(order_id)


@router.get(
    "/user/{user_id}/",
    response_model=list[OrderSummarySchema],
    status_code=status.HTTP_200_OK,
)
async def get_user_orders(
    user_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    service = OrderService(session)
    return await service.get_user_orders(user_id)


@router.post(
    "/product/",
    response_model=OrderReadSchema,
    status_code=status.HTTP_200_OK,
)
async def add_product_to_order(
    data: AddProductRequest,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    service = OrderService(session)
    return await service.add_product_to_order(
        order_id=data.order_id,
        product_id=data.product_id,
        count=data.count,
    )


@router.post(
    "/products",
    response_model=OrderReadSchema,
    status_code=status.HTTP_200_OK,
)
async def add_products_to_order(
    data: OrderProductsAddSchema,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    service = OrderService(session)
    return await service.add_products_to_order(data)


@router.put(
    "/products",
    response_model=OrderReadSchema,
    status_code=status.HTTP_200_OK,
)
async def replace_products_in_order(
    data: OrderProductsReplaceSchema,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    service = OrderService(session)
    return await service.replace_products_in_order(data)


@router.patch(
    "/products/",
    response_model=OrderReadSchema,
    status_code=status.HTTP_200_OK,
)
async def update_product_count(
    data: UpdateProductRequest,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    service = OrderService(session)
    return await service.update_product_count(
        order_id=data.order_id,
        product_id=data.product_id,
        data=OrderProductUpdateSchema(count=data.count),
    )


@router.delete(
    "/products/",
    response_model=OrderReadSchema,
    status_code=status.HTTP_200_OK,
)
async def remove_product_from_order(
    data: RemoveProductRequest,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    service = OrderService(session)
    return await service.remove_product_from_order(
        order_id=data.order_id,
        product_id=data.product_id,
    )


@router.post(
    "/checkout/",
    response_model=OrderReadSchema,
    status_code=status.HTTP_200_OK,
)
async def checkout_order(
    data: CheckoutRequest,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    service = OrderService(session)
    return await service.checkout_order(user_id=data.user_id, order_id=data.order_id)


@router.post(
    "/cancel/",
    response_model=OrderReadSchema,
    status_code=status.HTTP_200_OK,
)
async def cancel_order(
    data: CancelOrderRequest,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    service = OrderService(session)
    return await service.cancel_order(user_id=data.user_id, order_id=data.order_id)
