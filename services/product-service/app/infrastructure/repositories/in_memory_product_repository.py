from typing import Dict, List, Optional

from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository


class InMemoryProductRepository(ProductRepository):
    def __init__(self) -> None:
        self._items: Dict[str, Product] = {}

    def save(self, product: Product) -> Product:
        self._items[product.id] = product
        return product

    def find_by_id(self, product_id: str) -> Optional[Product]:
        return self._items.get(product_id)

    def find_by_sku(self, sku: str) -> Optional[Product]:
        for p in self._items.values():
            if p.sku == sku and p.active:
                return p
        return None

    def find_all(self, include_inactive: bool = False) -> List[Product]:
        items = list(self._items.values())
        if not include_inactive:
            items = [p for p in items if p.active]
        return items

    def delete(self, product: Product) -> None:
        self._items.pop(product.id, None)

    def clear(self) -> None:
        self._items.clear()
