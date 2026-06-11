from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4


@dataclass
class Product:
    name: str
    sku: str
    unit: str
    minimum_stock: int
    description: Optional[str] = None
    category: Optional[str] = None
    active: bool = True
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def touch(self) -> None:
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        self.active = False
        self.touch()
