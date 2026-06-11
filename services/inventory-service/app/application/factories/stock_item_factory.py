from datetime import date

from app.application.schemas.stock_schemas import StockItemCreateRequest
from app.domain.entities.stock_item import StockItem
from app.domain.exceptions.inventory_exceptions import ValidationError


class StockItemFactory:
    @staticmethod
    def create(data: StockItemCreateRequest) -> StockItem:
        product_id = (data.product_id or "").strip()
        if not product_id:
            raise ValidationError("productId is required")
        if data.quantity < 0:
            raise ValidationError("quantity must be >= 0")
        if data.minimum_stock < 0:
            raise ValidationError("minimumStock must be >= 0")
        if data.expiration_date is not None and data.expiration_date <= date.today():
            raise ValidationError("expirationDate must be a future date")

        return StockItem(
            product_id=product_id,
            quantity=data.quantity,
            minimum_stock=data.minimum_stock,
            expiration_date=data.expiration_date,
            batch_code=data.batch_code,
        )
