from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from .base import Base
from .mixins.created_at import CreatedAtMixin


class RefreshToken(CreatedAtMixin, Base):
    __tablename__ = "refresh_tokens"

    token: Mapped[str] = mapped_column(unique=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
