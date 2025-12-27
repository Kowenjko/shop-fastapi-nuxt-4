import enum


class OrderStatus(str, enum.Enum):
    DRAFT = "draft"  # корзина
    PAID = "paid"  # оплачен
    CANCELED = "canceled"  # отменён
