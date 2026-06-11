import os
import sys

SERVICE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if SERVICE_ROOT not in sys.path:
    sys.path.insert(0, SERVICE_ROOT)

from fastapi.testclient import TestClient

from app.infrastructure.repositories.in_memory_product_repository import (
    InMemoryProductRepository,
)
from app.main import create_app
from app.presentation.routers import product_router as product_router_module


def before_scenario(context, scenario):
    product_router_module._repository = InMemoryProductRepository()
    context.client = TestClient(create_app())
    context.response = None
    context.created = {}


def after_scenario(context, scenario):
    context.client = None
