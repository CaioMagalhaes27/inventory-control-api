from app.domain.entities.movement_type import MovementType
from app.domain.entities.stock_movement import StockMovement


class MovementFactory:
    @staticmethod
    def create(
        stock_item_id: str,
        product_id: str,
        movement_type: MovementType,
        quantity: int,
        reason: str | None,
    ) -> StockMovement:
        return StockMovement(
            stock_item_id=stock_item_id,
            product_id=product_id,
            type=movement_type,
            quantity=quantity,
            reason=reason,
        )
