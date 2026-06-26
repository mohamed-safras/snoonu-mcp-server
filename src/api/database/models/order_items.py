from .base import Base
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class OrderItem(Base):
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(nullable=False)
    icing_text: Mapped[str | None] = mapped_column(Text)