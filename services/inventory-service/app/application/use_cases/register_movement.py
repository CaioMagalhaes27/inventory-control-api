from app.application.factories.movement_factory import MovementFactory
from app.application.use_cases.movement_strategy import get_strategy
from app.domain.entities.movement_type import MovementType
from app.domain.entities.stock_movement import StockMovement
from app.domain.exceptions.inventory_exceptions import StockItemNotFoundError
from app.domain.repositories.stock_item_repository import StockItemRepository
from app.domain.repositories.stock_movement_repository import StockMovementRepository


class RegisterMovementUseCase:
    def __init__(
        self,
        item_repository: StockItemRepository,
        movement_repository: StockMovementRepository,
    ):
        self.item_repository = item_repository
        self.movement_repository = movement_repository

    def execute(
        self,
        stock_item_id: str,
        movement_type: MovementType,
        quantity: int,
        reason: str | None,
    ) -> StockMovement:
        item = self.item_repository.find_by_id(stock_item_id)
        if item is None:
            raise StockItemNotFoundError(stock_item_id)

        strategy = get_strategy(movement_type)
        strategy.apply(item, quantity)
        item.touch()
        self.item_repository.save(item)

        movement = MovementFactory.create(
            stock_item_id=item.id,
            product_id=item.product_id,
            movement_type=movement_type,
            quantity=quantity,
            reason=reason,
        )
        return self.movement_repository.save(movement)
