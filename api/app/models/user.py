from typing import TYPE_CHECKING

from .base import Base

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models import Profile, Order, Post


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[str] = mapped_column()
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True)
    active: Mapped[bool] = mapped_column(default=True)

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")
    order: Mapped["Order"] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
