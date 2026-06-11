from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.database import Base


class StockItemModel(Base):
    __tablename__ = "stock_items"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    product_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    minimum_stock: Mapped[int] = mapped_column(Integer, nullable=False)
    expiration_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    batch_code: Mapped[str | None] = mapped_column(String, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class StockMovementModel(Base):
    __tablename__ = "stock_movements"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    stock_item_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    product_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str | None] = mapped_column(String, nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
