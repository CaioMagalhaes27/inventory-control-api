from typing import List

from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository


class ListProductsUseCase:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, include_inactive: bool = False) -> List[Product]:
        return self.repository.find_all(include_inactive=include_inactive)
