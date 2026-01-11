from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class OAuthAccount(Base):
    __tablename__ = "oauth_accounts"

    provider: Mapped[str] = mapped_column(String(32))  # github / google
    provider_account_id: Mapped[str] = mapped_column(String(128))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship(
        "User",
        back_populates="oauth_accounts",
        lazy="selectin",
    )

    __table_args__ = (UniqueConstraint("provider", "provider_account_id"),)
