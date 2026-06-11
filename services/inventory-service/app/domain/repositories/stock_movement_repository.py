from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.stock_movement import StockMovement


class StockMovementRepository(ABC):
    @abstractmethod
    def save(self, movement: StockMovement) -> StockMovement: ...

    @abstractmethod
    def find_by_item_id(self, stock_item_id: str) -> List[StockMovement]: ...
