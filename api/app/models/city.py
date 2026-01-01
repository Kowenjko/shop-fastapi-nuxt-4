from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

if TYPE_CHECKING:
    from .profile import Profile


class City(Base):
    __tablename__ = "cities"

    id: Mapped[str] = mapped_column(String(20), primary_key=True)  # UA0102001002
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    city_type: Mapped[str | None] = mapped_column(String(100))
    country: Mapped[str | None] = mapped_column(String(255))
    region: Mapped[str | None] = mapped_column(String(255))
    district: Mapped[str | None] = mapped_column(String(255))
    community: Mapped[str | None] = mapped_column(String(255))
    name_en: Mapped[str | None] = mapped_column(String(255))
    lat: Mapped[float | None] = mapped_column(nullable=True)
    lon: Mapped[float | None] = mapped_column(nullable=True)

    profile: Mapped["Profile"] = relationship(back_populates="city")

    @property
    def full_name(self) -> int:
        return f"{self.region}, {self.district} р-н, {self.community} громада, {self.city_type} {self.name}"

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name!r})"

    def __repr__(self):
        return f"<City id={self.id} name={self.name}>"
