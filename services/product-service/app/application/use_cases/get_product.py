from app.domain.entities.product import Product
from app.domain.exceptions.product_exceptions import ProductNotFoundError
from app.domain.repositories.product_repository import ProductRepository


class GetProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, product_id: str) -> Product:
        product = self.repository.find_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(product_id)
        return product
