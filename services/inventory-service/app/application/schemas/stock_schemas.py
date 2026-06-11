from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.domain.entities.movement_type import MovementType


class StockItemCreateRequest(BaseModel):
    product_id: str = Field(..., min_length=1, alias="productId")
    quantity: int = Field(..., ge=0)
    minimum_stock: int = Field(..., ge=0, alias="minimumStock")
    expiration_date: Optional[date] = Field(None, alias="expirationDate")
    batch_code: Optional[str] = Field(None, alias="batchCode")

    model_config = {"populate_by_name": True}


class StockMovementRequest(BaseModel):
    quantity: int = Field(..., gt=0)
    reason: Optional[str] = None


class StockItemResponse(BaseModel):
    id: str
    product_id: str = Field(..., alias="productId")
    quantity: int
    minimum_stock: int = Field(..., alias="minimumStock")
    expiration_date: Optional[date] = Field(None, alias="expirationDate")
    batch_code: Optional[str] = Field(None, alias="batchCode")
    active: bool
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {"populate_by_name": True}


class StockMovementResponse(BaseModel):
    id: str
    stock_item_id: str = Field(..., alias="stockItemId")
    product_id: str = Field(..., alias="productId")
    type: MovementType
    quantity: int
    reason: Optional[str] = None
    occurred_at: datetime = Field(..., alias="occurredAt")

    model_config = {"populate_by_name": True}
