from app.application.schemas.product_schemas import ProductUpdateRequest
from app.domain.entities.product import Product
from app.domain.exceptions.product_exceptions import (
    DuplicateSkuError,
    ProductNotFoundError,
    ValidationError,
)
from app.domain.repositories.product_repository import ProductRepository


class UpdateProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, product_id: str, data: ProductUpdateRequest) -> Product:
        product = self.repository.find_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)

        if data.name is not None:
            name = data.name.strip()
            if not name:
                raise ValidationError("name is required")
            product.name = name

        if data.sku is not None:
            sku = data.sku.strip()
            if not sku:
                raise ValidationError("sku is required")
            existing = self.repository.find_by_sku(sku)
            if existing and existing.id != product.id:
                raise DuplicateSkuError(sku)
            product.sku = sku

        if data.unit is not None:
            unit = data.unit.strip()
            if not unit:
                raise ValidationError("unit is required")
            product.unit = unit

        if data.minimum_stock is not None:
            if data.minimum_stock < 0:
                raise ValidationError("minimumStock must be >= 0")
            product.minimum_stock = data.minimum_stock

        if data.description is not None:
            product.description = data.description
        if data.category is not None:
            product.category = data.category

        product.touch()
        return self.repository.save(product)
