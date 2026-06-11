from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4

from app.domain.entities.movement_type import MovementType


@dataclass
class StockMovement:
    stock_item_id: str
    product_id: str
    type: MovementType
    quantity: int
    reason: Optional[str] = None
    id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=datetime.utcnow)
