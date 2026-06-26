from .base import Base
from sqlalchemy import String, Numeric, ARRAY, Text
from sqlalchemy.orm import Mapped, mapped_column

class City(Base):
    __tablename__ = "cities"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    lat: Mapped[float] = mapped_column(Numeric(9, 6), nullable=False)
    lng: Mapped[float] = mapped_column(Numeric(9, 6), nullable=False)
    aliases: Mapped[list[str] | None] = mapped_column(ARRAY(Text))