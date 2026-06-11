from typing import Dict, List, Optional

from app.domain.entities.stock_item import StockItem
from app.domain.repositories.stock_item_repository import StockItemRepository


class InMemoryStockItemRepository(StockItemRepository):
    def __init__(self) -> None:
        self._items: Dict[str, StockItem] = {}

    def save(self, item: StockItem) -> StockItem:
        self._items[item.id] = item
        return item

    def find_by_id(self, item_id: str) -> Optional[StockItem]:
        return self._items.get(item_id)

    def find_all(self) -> List[StockItem]:
        return [i for i in self._items.values() if i.active]

    def clear(self) -> None:
        self._items.clear()
