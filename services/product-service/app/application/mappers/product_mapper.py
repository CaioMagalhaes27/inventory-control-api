from app.application.schemas.product_schemas import ProductResponse
from app.domain.entities.product import Product


class ProductMapper:
    @staticmethod
    def to_response(product: Product) -> ProductResponse:
        return ProductResponse(
            id=product.id,
            name=product.name,
            sku=product.sku,
            unit=product.unit,
            minimumStock=product.minimum_stock,
            description=product.description,
            category=product.category,
            active=product.active,
            createdAt=product.created_at,
            updatedAt=product.updated_at,
        )
