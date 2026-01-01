from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .city import City


class Profile(UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    phone: Mapped[str | None] = mapped_column(String(40))
    age: Mapped[int | None] = mapped_column()

    city_id: Mapped[str] = mapped_column(ForeignKey("cities.id"), nullable=True)
    city: Mapped["City"] = relationship(back_populates="profile")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, first_name={self.first_name!r}, last_name={self.last_name!r}, user_id={self.user_id})"

    def __repr__(self):
        return str(self)
