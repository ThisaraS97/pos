from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.sale import SaleCreate, SaleResponse, SaleUpdate
from app.models.sale import Sale, SaleItem
from app.security import get_current_active_user
import uuid

router = APIRouter(prefix="/api/sales", tags=["Sales"])

def generate_reference_number():
    """Generate unique reference number"""
    return f"SALE-{uuid.uuid4().hex[:8].upper()}"

@router.get("", response_model=List[SaleResponse])
def get_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all sales"""
    return db.query(Sale).filter(Sale.is_deleted == False).offset(skip).limit(limit).all()

@router.post("", response_model=SaleResponse)
def create_sale(sale_data: SaleCreate, db: Session = Depends(get_db),
                current_user = Depends(get_current_active_user)):
    """Create a new sale"""
    # Calculate totals
    subtotal = sum(item.unit_price * item.quantity for item in sale_data.items)
    total_discount = sale_data.discount
    total_tax = sale_data.tax
    total = subtotal - total_discount + total_tax
    change = sale_data.amount_paid - total
    
    # Create sale
    db_sale = Sale(
        reference_number=generate_reference_number(),
        customer_id=sale_data.customer_id,
        cashier_id=current_user.id,
        subtotal=subtotal,
        discount=total_discount,
        tax=total_tax,
        total=total,
        amount_paid=sale_data.amount_paid,
        change=change,
        payment_method=sale_data.payment_method,
        notes=sale_data.notes
    )
    db.add(db_sale)
    db.flush()
    
    # Add sale items
    for item in sale_data.items:
        sale_item = SaleItem(
            sale_id=db_sale.id,
            product_id=item.product_id,
            product_name="",  # Should be fetched from product
            product_code="",  # Should be fetched from product
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount=item.discount,
            tax=item.tax,
            subtotal=item.unit_price * item.quantity
        )
        db.add(sale_item)
    
    db.commit()
    db.refresh(db_sale)
    return db_sale

@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    """Get a sale by ID"""
    sale = db.query(Sale).filter(Sale.id == sale_id, Sale.is_deleted == False).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(sale_id: int, sale_update: SaleUpdate, db: Session = Depends(get_db),
                current_user = Depends(get_current_active_user)):
    """Update a sale"""
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    update_data = sale_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sale, field, value)
    
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale

@router.delete("/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db),
                current_user = Depends(get_current_active_user)):
    """Delete/cancel a sale"""
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    sale.is_deleted = True
    db.add(sale)
    db.commit()
    return {"message": "Sale cancelled"}
