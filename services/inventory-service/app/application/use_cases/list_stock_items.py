from datetime import date, timedelta
from typing import List

from app.domain.entities.stock_item import StockItem
from app.domain.repositories.stock_item_repository import StockItemRepository


class ListStockItemsUseCase:
    def __init__(self, repository: StockItemRepository):
        self.repository = repository

    def execute(self) -> List[StockItem]:
        return self.repository.find_all()


class ListLowStockUseCase:
    def __init__(self, repository: StockItemRepository):
        self.repository = repository

    def execute(self) -> List[StockItem]:
        return [i for i in self.repository.find_all() if i.is_low_stock()]


class ListExpiringUseCase:
    def __init__(self, repository: StockItemRepository, window_days: int = 30):
        self.repository = repository
        self.window_days = window_days

    def execute(self) -> List[StockItem]:
        threshold = date.today() + timedelta(days=self.window_days)
        return [
            i
            for i in self.repository.find_all()
            if i.expiration_date is not None and i.expiration_date <= threshold
        ]
