from typing import TYPE_CHECKING, List
from sqlalchemy import ForeignKey, String, Text, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import func
from .base import Base


if TYPE_CHECKING:
    from .category import Category
    from .order import Order
    from .order_product_association import OrderProductAssociation


class Product(Base):

    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, default="", server_default="")
    price: Mapped[float] = mapped_column(Float, default=0.0, server_default="0.0")
    image_url: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship(back_populates="products")

    orders_details: Mapped[list["OrderProductAssociation"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
