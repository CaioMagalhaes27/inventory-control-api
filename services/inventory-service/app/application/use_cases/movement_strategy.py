from abc import ABC, abstractmethod

from app.domain.entities.movement_type import MovementType
from app.domain.entities.stock_item import StockItem
from app.domain.exceptions.inventory_exceptions import (
    InsufficientStockError,
    ValidationError,
)


class MovementStrategy(ABC):
    type: MovementType

    @abstractmethod
    def apply(self, item: StockItem, quantity: int) -> None: ...


class EntryStrategy(MovementStrategy):
    type = MovementType.ENTRY

    def apply(self, item: StockItem, quantity: int) -> None:
        if quantity <= 0:
            raise ValidationError("entry quantity must be > 0")
        item.quantity += quantity


class ExitStrategy(MovementStrategy):
    type = MovementType.EXIT

    def apply(self, item: StockItem, quantity: int) -> None:
        if quantity <= 0:
            raise ValidationError("exit quantity must be > 0")
        if item.quantity - quantity < 0:
            raise InsufficientStockError(item.quantity, quantity)
        item.quantity -= quantity


_STRATEGIES = {
    MovementType.ENTRY: EntryStrategy(),
    MovementType.EXIT: ExitStrategy(),
}


def get_strategy(movement_type: MovementType) -> MovementStrategy:
    return _STRATEGIES[movement_type]
