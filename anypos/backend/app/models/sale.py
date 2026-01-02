from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.sql import func
from app.database import Base
import enum

class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    CARD = "card"
    CHEQUE = "cheque"
    ONLINE = "online"
    CREDIT = "credit"

class SaleStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    reference_number = Column(String, unique=True, nullable=False, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    cashier_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    subtotal = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    amount_paid = Column(Float, default=0.0)
    change = Column(Float, default=0.0)
    
    payment_method = Column(Enum(PaymentMethod), default=PaymentMethod.CASH)
    status = Column(Enum(SaleStatus), default=SaleStatus.COMPLETED)
    
    notes = Column(String, nullable=True)
    is_deleted = Column(Boolean, default=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Sale {self.reference_number}>"

class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    product_name = Column(String, nullable=False)
    product_code = Column(String, nullable=False)
    
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    discount = Column(Float, default=0.0)
    tax = Column(Float, default=0.0)
    subtotal = Column(Float, nullable=False)
    
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<SaleItem {self.product_name}>"
