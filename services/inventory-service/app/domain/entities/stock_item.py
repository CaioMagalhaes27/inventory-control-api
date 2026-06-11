from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
from uuid import uuid4


@dataclass
class StockItem:
    product_id: str
    quantity: int
    minimum_stock: int
    expiration_date: Optional[date] = None
    batch_code: Optional[str] = None
    active: bool = True
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()

    def is_low_stock(self) -> bool:
        return self.quantity <= self.minimum_stock
