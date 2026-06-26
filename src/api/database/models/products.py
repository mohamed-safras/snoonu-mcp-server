from .base import Base
from .categories import Category
from datetime import datetime
from sqlalchemy import String, Numeric, Boolean, ForeignKey, ARRAY, Text, TIMESTAMP
from sqlalchemy.orm import  Mapped, mapped_column, relationship

class Product(Base):
    __tablename__ = "products"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text)
    description: Mapped[str | None] = mapped_column(Text)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    price_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    price_currency: Mapped[str] = mapped_column(String, default="QAR")
    compare_at_amount: Mapped[float | None] = mapped_column(Numeric(10, 2))
    in_stock: Mapped[bool] = mapped_column(Boolean, default=True)
    stock_level: Mapped[str | None] = mapped_column(String)
    image_url: Mapped[str | None] = mapped_column(Text)
    images: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    rating: Mapped[float | None] = mapped_column(Numeric(2, 1))
    url: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    category: Mapped["Category"] = relationship()