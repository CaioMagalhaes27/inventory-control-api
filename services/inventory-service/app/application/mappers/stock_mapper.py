from app.application.schemas.stock_schemas import (
    StockItemResponse,
    StockMovementResponse,
)
from app.domain.entities.stock_item import StockItem
from app.domain.entities.stock_movement import StockMovement


class StockItemMapper:
    @staticmethod
    def to_response(item: StockItem) -> StockItemResponse:
        return StockItemResponse(
            id=item.id,
            productId=item.product_id,
            quantity=item.quantity,
            minimumStock=item.minimum_stock,
            expirationDate=item.expiration_date,
            batchCode=item.batch_code,
            active=item.active,
            createdAt=item.created_at,
            updatedAt=item.updated_at,
        )


class StockMovementMapper:
    @staticmethod
    def to_response(movement: StockMovement) -> StockMovementResponse:
        return StockMovementResponse(
            id=movement.id,
            stockItemId=movement.stock_item_id,
            productId=movement.product_id,
            type=movement.type,
            quantity=movement.quantity,
            reason=movement.reason,
            occurredAt=movement.occurred_at,
        )
