from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

from app.models.enums import OrderStatus


class OrderBase(BaseModel):
    status: OrderStatus = Field(..., description="Order status")
    promocode: Optional[str] = Field(None, description="Promocode applied to the order")


class OrderItem(BaseModel):
    product_id: int
    name: str
    unit_price: int
    count: int
    total: int

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(OrderBase):
    id: int
    created_at: datetime

    items: List[OrderItem]

    total_items: int
    total_price: int

    model_config = ConfigDict(from_attributes=True)


class OrderUserResponse(BaseModel):
    id: int
    status: OrderStatus
    items: List[OrderItem]
    total_items: int
    total_price: int

    model_config = ConfigDict(from_attributes=True)


class OrderCreate(BaseModel):
    promocode: Optional[str] = None


class OrderProductUpdate(BaseModel):
    count: int


class AddProduct(BaseModel):
    user_id: int
    order_id: int
    product_id: int
    count: int = Field(..., ge=1)


class UpdateProduct(AddProduct):
    count: int = Field(..., ge=0)


class OrderProductBase(BaseModel):
    product_id: int
    count: int = Field(gt=0)


class OrderProductsAdd(BaseModel):
    order_id: int
    products: list[OrderProductBase]


class OrderProductsReplace(OrderProductsAdd):
    pass


class UserOrderBase(BaseModel):
    user_id: int
    order_id: int


class CancelOrder(UserOrderBase):
    pass


class CheckoutOrder(UserOrderBase):
    pass


class RemoveProduct(UserOrderBase):
    product_id: int
