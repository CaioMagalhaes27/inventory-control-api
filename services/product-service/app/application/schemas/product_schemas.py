from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ProductCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    sku: str = Field(..., min_length=1)
    unit: str = Field(..., min_length=1)
    minimum_stock: int = Field(..., ge=0, alias="minimumStock")
    description: Optional[str] = None
    category: Optional[str] = None

    model_config = {"populate_by_name": True}


class ProductUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    sku: Optional[str] = Field(None, min_length=1)
    unit: Optional[str] = Field(None, min_length=1)
    minimum_stock: Optional[int] = Field(None, ge=0, alias="minimumStock")
    description: Optional[str] = None
    category: Optional[str] = None

    model_config = {"populate_by_name": True}


class ProductResponse(BaseModel):
    id: str
    name: str
    sku: str
    unit: str
    minimum_stock: int = Field(..., alias="minimumStock")
    description: Optional[str] = None
    category: Optional[str] = None
    active: bool
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")

    model_config = {"populate_by_name": True}
