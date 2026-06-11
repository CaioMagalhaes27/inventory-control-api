from app.application.factories.product_factory import ProductFactory
from app.application.schemas.product_schemas import ProductCreateRequest
from app.domain.entities.product import Product
from app.domain.exceptions.product_exceptions import DuplicateSkuError
from app.domain.repositories.product_repository import ProductRepository


class CreateProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, data: ProductCreateRequest) -> Product:
        if self.repository.find_by_sku(data.sku.strip()):
            raise DuplicateSkuError(data.sku)
        product = ProductFactory.create(data)
        return self.repository.save(product)
