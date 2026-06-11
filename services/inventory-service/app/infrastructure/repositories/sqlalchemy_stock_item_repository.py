from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.domain.entities.stock_item import StockItem
from app.domain.repositories.stock_item_repository import StockItemRepository
from app.infrastructure.database import SessionLocal, init_database
from app.infrastructure.database.models import StockItemModel


class SqlAlchemyStockItemRepository(StockItemRepository):
    def __init__(self, session_factory: sessionmaker[Session] = SessionLocal) -> None:
        init_database()
        self.session_factory = session_factory

    def save(self, item: StockItem) -> StockItem:
        with self.session_factory() as session:
            model = session.get(StockItemModel, item.id)
            if model is None:
                model = StockItemModel(id=item.id)
                session.add(model)

            self._fill_model(model, item)
            session.commit()
            session.refresh(model)
            return self._to_entity(model)

    def find_by_id(self, item_id: str) -> Optional[StockItem]:
        with self.session_factory() as session:
            model = session.get(StockItemModel, item_id)
            if model is None or not model.active:
                return None
            return self._to_entity(model)

    def find_all(self) -> List[StockItem]:
        with self.session_factory() as session:
            stmt = (
                select(StockItemModel)
                .where(StockItemModel.active.is_(True))
                .order_by(StockItemModel.created_at)
            )
            models = session.execute(stmt).scalars().all()
            return [self._to_entity(model) for model in models]

    @staticmethod
    def _fill_model(model: StockItemModel, item: StockItem) -> None:
        model.product_id = item.product_id
        model.quantity = item.quantity
        model.minimum_stock = item.minimum_stock
        model.expiration_date = item.expiration_date
        model.batch_code = item.batch_code
        model.active = item.active
        model.created_at = item.created_at
        model.updated_at = item.updated_at

    @staticmethod
    def _to_entity(model: StockItemModel) -> StockItem:
        return StockItem(
            id=model.id,
            product_id=model.product_id,
            quantity=model.quantity,
            minimum_stock=model.minimum_stock,
            expiration_date=model.expiration_date,
            batch_code=model.batch_code,
            active=model.active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
