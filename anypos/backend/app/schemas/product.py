from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    cost_price: float = 0.0
    selling_price: float = 0.0
    quantity_in_stock: int = 0
    minimum_stock: int = 0
    barcode: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    cost_price: Optional[float] = None
    selling_price: Optional[float] = None
    minimum_stock: Optional[int] = None
    barcode: Optional[str] = None

class ProductResponse(ProductBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
