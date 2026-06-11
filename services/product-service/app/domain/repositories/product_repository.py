from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.product import Product


class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> Product: ...

    @abstractmethod
    def find_by_id(self, product_id: str) -> Optional[Product]: ...

    @abstractmethod
    def find_by_sku(self, sku: str) -> Optional[Product]: ...

    @abstractmethod
    def find_all(self, include_inactive: bool = False) -> List[Product]: ...

    @abstractmethod
    def delete(self, product: Product) -> None: ...
