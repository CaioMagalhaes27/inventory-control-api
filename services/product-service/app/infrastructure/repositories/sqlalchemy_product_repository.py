from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.domain.entities.product import Product
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.database import SessionLocal, init_database
from app.infrastructure.database.models import ProductModel


class SqlAlchemyProductRepository(ProductRepository):
    def __init__(self, session_factory: sessionmaker[Session] = SessionLocal) -> None:
        init_database()
        self.session_factory = session_factory

    def save(self, product: Product) -> Product:
        with self.session_factory() as session:
            model = session.get(ProductModel, product.id)
            if model is None:
                model = ProductModel(id=product.id)
                session.add(model)

            self._fill_model(model, product)
            session.commit()
            session.refresh(model)
            return self._to_entity(model)

    def find_by_id(self, product_id: str) -> Optional[Product]:
        with self.session_factory() as session:
            model = session.get(ProductModel, product_id)
            return self._to_entity(model) if model else None

    def find_by_sku(self, sku: str) -> Optional[Product]:
        with self.session_factory() as session:
            stmt = select(ProductModel).where(
                ProductModel.sku == sku,
                ProductModel.active.is_(True),
            )
            model = session.execute(stmt).scalars().first()
            return self._to_entity(model) if model else None

    def find_all(self, include_inactive: bool = False) -> List[Product]:
        with self.session_factory() as session:
            stmt = select(ProductModel)
            if not include_inactive:
                stmt = stmt.where(ProductModel.active.is_(True))
            models = session.execute(stmt.order_by(ProductModel.created_at)).scalars().all()
            return [self._to_entity(model) for model in models]

    def delete(self, product: Product) -> None:
        with self.session_factory() as session:
            model = session.get(ProductModel, product.id)
            if model:
                session.delete(model)
                session.commit()

    @staticmethod
    def _fill_model(model: ProductModel, product: Product) -> None:
        model.name = product.name
        model.description = product.description
        model.sku = product.sku
        model.category = product.category
        model.unit = product.unit
        model.minimum_stock = product.minimum_stock
        model.active = product.active
        model.created_at = product.created_at
        model.updated_at = product.updated_at

    @staticmethod
    def _to_entity(model: ProductModel) -> Product:
        return Product(
            id=model.id,
            name=model.name,
            description=model.description,
            sku=model.sku,
            category=model.category,
            unit=model.unit,
            minimum_stock=model.minimum_stock,
            active=model.active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
