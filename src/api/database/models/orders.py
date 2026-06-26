from .base import Base
from datetime import datetime
from sqlalchemy import String, Numeric, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSONB

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    status: Mapped[str] = mapped_column(String, default="pending_payment")
    total_amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String, default="QAR")
    recipient: Mapped[dict] = mapped_column(JSONB, nullable=False)
    delivery: Mapped[dict] = mapped_column(JSONB, nullable=False)
    sender: Mapped[dict] = mapped_column(JSONB, nullable=False)
    gift_message: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=datetime.utcnow)
    expires_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))