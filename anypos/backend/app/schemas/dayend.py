from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DayEndCreate(BaseModel):
    opening_balance: float = 0.0
    notes: Optional[str] = None


class DayEndClose(BaseModel):
    actual_cash: float
    notes: Optional[str] = None


class DayEndPaymentBreakdown(BaseModel):
    cash: float
    card: float
    cheque: float
    online: float
    credit: float


class DayEndSalesSummary(BaseModel):
    total_sales: int
    total_revenue: float
    total_discount: float
    total_tax: float


class DayEndCashReconciliation(BaseModel):
    opening_balance: float
    expected_cash: float
    actual_cash: float
    variance: float
    closing_balance: float


class DayEndSummary(BaseModel):
    id: int
    cashier_id: int
    opened_at: datetime
    closed_at: Optional[datetime]
    is_closed: bool
    sales_summary: DayEndSalesSummary
    payment_breakdown: DayEndPaymentBreakdown
    cash_reconciliation: DayEndCashReconciliation
    notes: Optional[str] = None


class DayEndResponse(BaseModel):
    id: int
    cashier_id: int
    total_sales_count: int
    total_revenue: float
    total_discount: float
    total_tax: float
    cash_sales: float
    card_sales: float
    cheque_sales: float
    online_sales: float
    credit_sales: float
    expected_cash: float
    actual_cash: float
    cash_variance: float
    opening_balance: float
    closing_balance: float
    is_closed: bool
    opened_at: datetime
    closed_at: Optional[datetime]
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class DayEndList(BaseModel):
    id: int
    cashier_id: int
    opened_at: datetime
    closed_at: Optional[datetime]
    is_closed: bool
    total_revenue: float
    total_sales_count: int
    cash_variance: float

    class Config:
        from_attributes = True
