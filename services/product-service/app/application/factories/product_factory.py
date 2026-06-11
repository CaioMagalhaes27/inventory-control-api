from app.application.schemas.product_schemas import ProductCreateRequest
from app.domain.entities.product import Product
from app.domain.exceptions.product_exceptions import ValidationError


class ProductFactory:
    @staticmethod
    def create(data: ProductCreateRequest) -> Product:
        name = (data.name or "").strip()
        sku = (data.sku or "").strip()
        unit = (data.unit or "").strip()

        if not name:
            raise ValidationError("name is required")
        if not sku:
            raise ValidationError("sku is required")
        if not unit:
            raise ValidationError("unit is required")
        if data.minimum_stock < 0:
            raise ValidationError("minimumStock must be >= 0")

        return Product(
            name=name,
            sku=sku,
            unit=unit,
            minimum_stock=data.minimum_stock,
            description=data.description,
            category=data.category,
        )
