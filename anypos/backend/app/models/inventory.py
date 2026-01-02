from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from app.database import Base
import enum

class AdjustmentType(str, enum.Enum):
    STOCK_IN = "stock_in"
    STOCK_OUT = "stock_out"
    DAMAGED = "damaged"
    LOST = "lost"
    RETURN = "return"

class StockAdjustment(Base):
    __tablename__ = "stock_adjustments"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    adjustment_type = Column(Enum(AdjustmentType), nullable=False)
    quantity = Column(Integer, nullable=False)
    reason = Column(String, nullable=True)
    reference = Column(String, nullable=True)
    
    adjusted_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<StockAdjustment {self.id}>"
