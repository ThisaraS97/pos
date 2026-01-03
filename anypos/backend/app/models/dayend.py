from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from datetime import datetime

class DayEnd(Base):
    __tablename__ = "dayends"

    id = Column(Integer, primary_key=True, index=True)
    cashier_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Sales summary
    total_sales_count = Column(Integer, default=0)
    total_revenue = Column(Float, default=0.0)
    total_discount = Column(Float, default=0.0)
    total_tax = Column(Float, default=0.0)
    
    # Payment method breakdown
    cash_sales = Column(Float, default=0.0)
    card_sales = Column(Float, default=0.0)
    cheque_sales = Column(Float, default=0.0)
    online_sales = Column(Float, default=0.0)
    credit_sales = Column(Float, default=0.0)
    
    # Cash reconciliation
    expected_cash = Column(Float, default=0.0)  # Expected based on sales
    actual_cash = Column(Float, default=0.0)    # Actual counted
    cash_variance = Column(Float, default=0.0)  # Difference
    
    # Day end metadata
    opening_balance = Column(Float, default=0.0)
    closing_balance = Column(Float, default=0.0)
    notes = Column(String, nullable=True)
    
    # Status
    is_closed = Column(Boolean, default=False)
    
    # Timestamps
    opened_at = Column(DateTime, server_default=func.now())
    closed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    cashier = relationship("User", foreign_keys=[cashier_id])

    def __repr__(self):
        return f"<DayEnd {self.id} - {self.opened_at.date() if self.opened_at else 'Unknown'}>"


class DayEndTransaction(Base):
    __tablename__ = "dayend_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    dayend_id = Column(Integer, ForeignKey("dayends.id"), nullable=False)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    dayend = relationship("DayEnd")

    def __repr__(self):
        return f"<DayEndTransaction dayend_id={self.dayend_id}>"
