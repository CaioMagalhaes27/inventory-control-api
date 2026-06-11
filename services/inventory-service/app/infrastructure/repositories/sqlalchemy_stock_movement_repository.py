from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker

from app.domain.entities.movement_type import MovementType
from app.domain.entities.stock_movement import StockMovement
from app.domain.repositories.stock_movement_repository import StockMovementRepository
from app.infrastructure.database import SessionLocal, init_database
from app.infrastructure.database.models import StockMovementModel


class SqlAlchemyStockMovementRepository(StockMovementRepository):
    def __init__(self, session_factory: sessionmaker[Session] = SessionLocal) -> None:
        init_database()
        self.session_factory = session_factory

    def save(self, movement: StockMovement) -> StockMovement:
        with self.session_factory() as session:
            model = session.get(StockMovementModel, movement.id)
            if model is None:
                model = StockMovementModel(id=movement.id)
                session.add(model)

            self._fill_model(model, movement)
            session.commit()
            session.refresh(model)
            return self._to_entity(model)

    def find_by_item_id(self, stock_item_id: str) -> List[StockMovement]:
        with self.session_factory() as session:
            stmt = (
                select(StockMovementModel)
                .where(StockMovementModel.stock_item_id == stock_item_id)
                .order_by(StockMovementModel.occurred_at)
            )
            models = session.execute(stmt).scalars().all()
            return [self._to_entity(model) for model in models]

    @staticmethod
    def _fill_model(model: StockMovementModel, movement: StockMovement) -> None:
        model.stock_item_id = movement.stock_item_id
        model.product_id = movement.product_id
        model.type = movement.type.value
        model.quantity = movement.quantity
        model.reason = movement.reason
        model.occurred_at = movement.occurred_at

    @staticmethod
    def _to_entity(model: StockMovementModel) -> StockMovement:
        return StockMovement(
            id=model.id,
            stock_item_id=model.stock_item_id,
            product_id=model.product_id,
            type=MovementType(model.type),
            quantity=model.quantity,
            reason=model.reason,
            occurred_at=model.occurred_at,
        )
