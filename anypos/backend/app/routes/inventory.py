from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.models.inventory import StockAdjustment, AdjustmentType
from app.models.product import Product
from app.security import get_current_active_user

router = APIRouter(prefix="/api/inventory", tags=["Inventory"])

class StockAdjustmentCreate(BaseModel):
    product_id: int
    adjustment_type: AdjustmentType
    quantity: int
    reason: str = ""
    reference: str = ""

class StockAdjustmentResponse(BaseModel):
    id: int
    product_id: int
    adjustment_type: AdjustmentType
    quantity: int
    reason: str
    reference: str
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("", response_model=List[StockAdjustmentResponse])
def get_stock_adjustments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get stock adjustments"""
    return db.query(StockAdjustment).offset(skip).limit(limit).all()

@router.post("", response_model=StockAdjustmentResponse)
def create_stock_adjustment(adjustment: StockAdjustmentCreate, db: Session = Depends(get_db),
                           current_user = Depends(get_current_active_user)):
    """Create a stock adjustment"""
    product = db.query(Product).filter(Product.id == adjustment.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Update product quantity
    if adjustment.adjustment_type == AdjustmentType.STOCK_IN:
        product.quantity_in_stock += adjustment.quantity
    else:
        product.quantity_in_stock = max(0, product.quantity_in_stock - adjustment.quantity)
    
    db_adjustment = StockAdjustment(
        product_id=adjustment.product_id,
        adjustment_type=adjustment.adjustment_type,
        quantity=adjustment.quantity,
        reason=adjustment.reason,
        reference=adjustment.reference,
        adjusted_by=current_user.id
    )
    
    db.add(product)
    db.add(db_adjustment)
    db.commit()
    db.refresh(db_adjustment)
    return db_adjustment
