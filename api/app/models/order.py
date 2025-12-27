from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.enums import OrderStatus
from .base import Base
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .product import Product
    from .order_product_association import OrderProductAssociation


class Order(UserRelationMixin, Base):
    _user_id_unique = False

    # Enum PostgreSQL, храним как строку
    status: Mapped[str] = mapped_column(
        SAEnum(
            OrderStatus,
            name="order_status",
            values_callable=lambda obj: [e.value for e in obj],
        ),
        default=OrderStatus.DRAFT.value,
        server_default=OrderStatus.DRAFT.value,
        index=True,
        nullable=False,
    )

    promocode: Mapped[str | None]

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=datetime.utcnow,
    )

    # association between Parent -> Association -> Child
    products_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )

    @property
    def total_price(self) -> int:
        return sum(item.count * item.unit_price for item in self.products_details)

    @property
    def total_items(self) -> int:
        return sum(item.count for item in self.products_details)
