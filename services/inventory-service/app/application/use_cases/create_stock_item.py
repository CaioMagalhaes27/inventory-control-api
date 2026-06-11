from app.application.factories.stock_item_factory import StockItemFactory
from app.application.schemas.stock_schemas import StockItemCreateRequest
from app.domain.entities.stock_item import StockItem
from app.domain.repositories.stock_item_repository import StockItemRepository


class CreateStockItemUseCase:
    def __init__(self, repository: StockItemRepository):
        self.repository = repository

    def execute(self, data: StockItemCreateRequest) -> StockItem:
        item = StockItemFactory.create(data)
        return self.repository.save(item)
