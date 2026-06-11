from app.domain.exceptions.product_exceptions import ProductNotFoundError
from app.domain.repositories.product_repository import ProductRepository


class DeleteProductUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, product_id: str) -> None:
        product = self.repository.find_by_id(product_id)
        if product is None or not product.active:
            raise ProductNotFoundError(product_id)
        product.deactivate()
        self.repository.save(product)
