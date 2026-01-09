from typing import TYPE_CHECKING

from .base import Base
from .mixins.created_at import CreatedAtMixin, utcnow

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

if TYPE_CHECKING:
    from app.models import Profile, Order, Post


class User(CreatedAtMixin, Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)
    password_hash: Mapped[bytes] = mapped_column(nullable=False)
    email: Mapped[str | None] = mapped_column(String(64), unique=True, nullable=True)
    role: Mapped[str] = mapped_column(default="user", server_default="user")
    active: Mapped[bool] = mapped_column(Boolean, default=True)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utcnow,
        onupdate=utcnow,
        nullable=True,
    )

    posts: Mapped[list["Post"]] = relationship(back_populates="user")
    profile: Mapped["Profile"] = relationship(back_populates="user")
    order: Mapped["Order"] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r}. email={self.email!r})"

    def __repr__(self):
        return str(self)
