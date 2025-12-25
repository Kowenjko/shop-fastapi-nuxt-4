from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Profile(UserRelationMixin, Base):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    phone: Mapped[str | None] = mapped_column(String(40))
    address: Mapped[str | None] = mapped_column(String(255))
    age: Mapped[int | None] = mapped_column()

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, first_name={self.first_name!r}, last_name={self.last_name!r}, user_id={self.user_id})"

    def __repr__(self):
        return str(self)
