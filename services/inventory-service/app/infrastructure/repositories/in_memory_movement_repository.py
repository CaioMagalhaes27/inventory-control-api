from typing import Dict, List

from app.domain.entities.stock_movement import StockMovement
from app.domain.repositories.stock_movement_repository import StockMovementRepository


class InMemoryStockMovementRepository(StockMovementRepository):
    def __init__(self) -> None:
        self._items: Dict[str, StockMovement] = {}

    def save(self, movement: StockMovement) -> StockMovement:
        self._items[movement.id] = movement
        return movement

    def find_by_item_id(self, stock_item_id: str) -> List[StockMovement]:
        return [m for m in self._items.values() if m.stock_item_id == stock_item_id]

    def clear(self) -> None:
        self._items.clear()
