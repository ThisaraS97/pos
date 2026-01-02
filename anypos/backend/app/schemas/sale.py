from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.sale import PaymentMethod, SaleStatus

class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    discount: float = 0.0
    tax: float = 0.0

class SaleItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    product_code: str
    quantity: int
    unit_price: float
    discount: float
    tax: float
    subtotal: float

    class Config:
        from_attributes = True

class SaleCreate(BaseModel):
    customer_id: Optional[int] = None
    payment_method: PaymentMethod = PaymentMethod.CASH
    discount: float = 0.0
    tax: float = 0.0
    amount_paid: float = 0.0
    notes: Optional[str] = None
    items: List[SaleItemCreate]

class SaleUpdate(BaseModel):
    status: Optional[SaleStatus] = None
    notes: Optional[str] = None

class SaleResponse(BaseModel):
    id: int
    reference_number: str
    customer_id: Optional[int] = None
    cashier_id: int
    subtotal: float
    discount: float
    tax: float
    total: float
    amount_paid: float
    change: float
    payment_method: PaymentMethod
    status: SaleStatus
    created_at: datetime

    class Config:
        from_attributes = True
