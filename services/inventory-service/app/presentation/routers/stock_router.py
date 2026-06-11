from typing import List

from fastapi import APIRouter, Depends, status

from app.application.mappers.stock_mapper import StockItemMapper, StockMovementMapper
from app.application.schemas.stock_schemas import (
    StockItemCreateRequest,
    StockItemResponse,
    StockMovementRequest,
    StockMovementResponse,
)
from app.application.use_cases.create_stock_item import CreateStockItemUseCase
from app.application.use_cases.get_stock_item import GetStockItemUseCase
from app.application.use_cases.list_stock_items import (
    ListExpiringUseCase,
    ListLowStockUseCase,
    ListStockItemsUseCase,
)
from app.application.use_cases.register_movement import RegisterMovementUseCase
from app.domain.entities.movement_type import MovementType
from app.domain.repositories.stock_item_repository import StockItemRepository
from app.domain.repositories.stock_movement_repository import StockMovementRepository
from app.infrastructure.repositories.in_memory_movement_repository import (
    InMemoryStockMovementRepository,
)
from app.infrastructure.repositories.in_memory_stock_item_repository import (
    InMemoryStockItemRepository,
)

router = APIRouter(prefix="/api/stock-items", tags=["stock-items"])

_item_repository: StockItemRepository = InMemoryStockItemRepository()
_movement_repository: StockMovementRepository = InMemoryStockMovementRepository()


def get_item_repository() -> StockItemRepository:
    return _item_repository


def get_movement_repository() -> StockMovementRepository:
    return _movement_repository


@router.post("", response_model=StockItemResponse, status_code=status.HTTP_201_CREATED)
def create_stock_item(
    payload: StockItemCreateRequest,
    repository: StockItemRepository = Depends(get_item_repository),
) -> StockItemResponse:
    item = CreateStockItemUseCase(repository).execute(payload)
    return StockItemMapper.to_response(item)


@router.get("", response_model=List[StockItemResponse])
def list_stock_items(
    repository: StockItemRepository = Depends(get_item_repository),
) -> List[StockItemResponse]:
    items = ListStockItemsUseCase(repository).execute()
    return [StockItemMapper.to_response(i) for i in items]


@router.get("/low-stock", response_model=List[StockItemResponse])
def list_low_stock(
    repository: StockItemRepository = Depends(get_item_repository),
) -> List[StockItemResponse]:
    items = ListLowStockUseCase(repository).execute()
    return [StockItemMapper.to_response(i) for i in items]


@router.get("/expiring", response_model=List[StockItemResponse])
def list_expiring(
    repository: StockItemRepository = Depends(get_item_repository),
) -> List[StockItemResponse]:
    items = ListExpiringUseCase(repository).execute()
    return [StockItemMapper.to_response(i) for i in items]


@router.get("/{item_id}", response_model=StockItemResponse)
def get_stock_item(
    item_id: str,
    repository: StockItemRepository = Depends(get_item_repository),
) -> StockItemResponse:
    item = GetStockItemUseCase(repository).execute(item_id)
    return StockItemMapper.to_response(item)


@router.post(
    "/{item_id}/entries",
    response_model=StockMovementResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_entry(
    item_id: str,
    payload: StockMovementRequest,
    item_repository: StockItemRepository = Depends(get_item_repository),
    movement_repository: StockMovementRepository = Depends(get_movement_repository),
) -> StockMovementResponse:
    movement = RegisterMovementUseCase(item_repository, movement_repository).execute(
        stock_item_id=item_id,
        movement_type=MovementType.ENTRY,
        quantity=payload.quantity,
        reason=payload.reason,
    )
    return StockMovementMapper.to_response(movement)


@router.post(
    "/{item_id}/exits",
    response_model=StockMovementResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_exit(
    item_id: str,
    payload: StockMovementRequest,
    item_repository: StockItemRepository = Depends(get_item_repository),
    movement_repository: StockMovementRepository = Depends(get_movement_repository),
) -> StockMovementResponse:
    movement = RegisterMovementUseCase(item_repository, movement_repository).execute(
        stock_item_id=item_id,
        movement_type=MovementType.EXIT,
        quantity=payload.quantity,
        reason=payload.reason,
    )
    return StockMovementMapper.to_response(movement)
