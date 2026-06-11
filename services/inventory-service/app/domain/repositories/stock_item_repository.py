from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.stock_item import StockItem


class StockItemRepository(ABC):
    @abstractmethod
    def save(self, item: StockItem) -> StockItem: ...

    @abstractmethod
    def find_by_id(self, item_id: str) -> Optional[StockItem]: ...

    @abstractmethod
    def find_all(self) -> List[StockItem]: ...
