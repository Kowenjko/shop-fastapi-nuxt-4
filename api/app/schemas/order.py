from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

from app.models.enums import OrderStatus


# -------- Products inside Order --------


class OrderItemSchema(BaseModel):
    product_id: int
    name: str
    unit_price: int
    count: int
    total: int

    model_config = ConfigDict(from_attributes=True)


# -------- Order --------


class OrderReadSchema(BaseModel):
    id: int
    status: OrderStatus
    promocode: Optional[str]
    created_at: datetime

    items: List[OrderItemSchema]

    total_items: int
    total_price: int

    model_config = ConfigDict(from_attributes=True)


class OrderSummarySchema(BaseModel):
    id: int
    status: OrderStatus
    total_items: int
    total_price: int


# -------- Create / Update --------


class OrderCreateSchema(BaseModel):
    promocode: Optional[str] = None


class OrderProductUpdateSchema(BaseModel):
    count: int


class AddProductRequest(BaseModel):
    user_id: int
    order_id: int
    product_id: int
    count: int = Field(..., ge=1)


class OrderProductAddItemSchema(BaseModel):
    product_id: int
    count: int = Field(gt=0)


class OrderProductsAddSchema(BaseModel):
    order_id: int
    products: list[OrderProductAddItemSchema]


class OrderProductCreate(BaseModel):
    product_id: int
    count: int = Field(gt=0)


class OrderProductReplaceItemSchema(BaseModel):
    product_id: int
    count: int = Field(gt=0)


class OrderProductsReplaceSchema(BaseModel):
    order_id: int
    products: list[OrderProductReplaceItemSchema]


class UpdateProductRequest(BaseModel):
    user_id: int
    order_id: int
    product_id: int
    count: int = Field(..., ge=0)


class RemoveProductRequest(BaseModel):
    user_id: int
    order_id: int
    product_id: int


class CancelOrderRequest(BaseModel):
    user_id: int
    order_id: int


class CheckoutRequest(BaseModel):
    user_id: int
    order_id: int
