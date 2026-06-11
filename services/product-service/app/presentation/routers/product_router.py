from typing import List

from fastapi import APIRouter, Depends, status

from app.application.mappers.product_mapper import ProductMapper
from app.application.schemas.product_schemas import (
    ProductCreateRequest,
    ProductResponse,
    ProductUpdateRequest,
)
from app.application.use_cases.create_product import CreateProductUseCase
from app.application.use_cases.delete_product import DeleteProductUseCase
from app.application.use_cases.get_product import GetProductUseCase
from app.application.use_cases.list_products import ListProductsUseCase
from app.application.use_cases.update_product import UpdateProductUseCase
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.repositories.sqlalchemy_product_repository import (
    SqlAlchemyProductRepository,
)

router = APIRouter(prefix="/api/products", tags=["products"])

_repository: ProductRepository = SqlAlchemyProductRepository()


def get_repository() -> ProductRepository:
    return _repository


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreateRequest,
    repository: ProductRepository = Depends(get_repository),
) -> ProductResponse:
    product = CreateProductUseCase(repository).execute(payload)
    return ProductMapper.to_response(product)


@router.get("", response_model=List[ProductResponse])
def list_products(
    repository: ProductRepository = Depends(get_repository),
) -> List[ProductResponse]:
    products = ListProductsUseCase(repository).execute()
    return [ProductMapper.to_response(p) for p in products]


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: str, repository: ProductRepository = Depends(get_repository)
) -> ProductResponse:
    product = GetProductUseCase(repository).execute(product_id)
    return ProductMapper.to_response(product)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    payload: ProductUpdateRequest,
    repository: ProductRepository = Depends(get_repository),
) -> ProductResponse:
    product = UpdateProductUseCase(repository).execute(product_id, payload)
    return ProductMapper.to_response(product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: str, repository: ProductRepository = Depends(get_repository)
) -> None:
    DeleteProductUseCase(repository).execute(product_id)
