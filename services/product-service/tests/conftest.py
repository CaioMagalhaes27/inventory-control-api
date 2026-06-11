import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import create_app  # noqa: E402
from app.presentation.routers import product_router as product_router_module  # noqa: E402
from app.infrastructure.repositories.in_memory_product_repository import (  # noqa: E402
    InMemoryProductRepository,
)


@pytest.fixture()
def client() -> TestClient:
    product_router_module._repository = InMemoryProductRepository()
    app = create_app()
    return TestClient(app)


@pytest.fixture()
def valid_payload() -> dict:
    return {
        "name": "Arroz 1kg",
        "sku": "SKU-001",
        "unit": "kg",
        "minimumStock": 5,
        "description": "Arroz branco",
        "category": "Alimentos",
    }
