import os
import sys
from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import create_app  # noqa: E402
from app.presentation.routers import stock_router as stock_router_module  # noqa: E402
from app.infrastructure.repositories.in_memory_movement_repository import (  # noqa: E402
    InMemoryStockMovementRepository,
)
from app.infrastructure.repositories.in_memory_stock_item_repository import (  # noqa: E402
    InMemoryStockItemRepository,
)


@pytest.fixture()
def client() -> TestClient:
    stock_router_module._item_repository = InMemoryStockItemRepository()
    stock_router_module._movement_repository = InMemoryStockMovementRepository()
    app = create_app()
    return TestClient(app)


@pytest.fixture()
def future_date() -> str:
    return (date.today() + timedelta(days=60)).isoformat()


@pytest.fixture()
def near_expiration_date() -> str:
    return (date.today() + timedelta(days=10)).isoformat()


@pytest.fixture()
def valid_payload(future_date) -> dict:
    return {
        "productId": "prod-1",
        "quantity": 10,
        "minimumStock": 5,
        "expirationDate": future_date,
        "batchCode": "B-001",
    }
