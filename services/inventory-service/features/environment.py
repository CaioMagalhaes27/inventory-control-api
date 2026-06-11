import os
import sys

SERVICE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SERVICE_ROOT not in sys.path:
    sys.path.insert(0, SERVICE_ROOT)

from fastapi.testclient import TestClient

from app.infrastructure.repositories.in_memory_movement_repository import (
    InMemoryStockMovementRepository,
)
from app.infrastructure.repositories.in_memory_stock_item_repository import (
    InMemoryStockItemRepository,
)
from app.main import create_app
from app.presentation.routers import stock_router as stock_router_module


def before_scenario(context, scenario):
    stock_router_module._item_repository = InMemoryStockItemRepository()
    stock_router_module._movement_repository = InMemoryStockMovementRepository()
    context.client = TestClient(create_app())
    context.response = None
    context.last_item = None


def after_scenario(context, scenario):
    context.client = None
