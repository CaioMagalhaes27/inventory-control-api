from app.domain.entities.stock_item import StockItem
from app.domain.exceptions.inventory_exceptions import StockItemNotFoundError
from app.domain.repositories.stock_item_repository import StockItemRepository


class GetStockItemUseCase:
    def __init__(self, repository: StockItemRepository):
        self.repository = repository

    def execute(self, item_id: str) -> StockItem:
        item = self.repository.find_by_id(item_id)
        if item is None:
            raise StockItemNotFoundError(item_id)
        return item
