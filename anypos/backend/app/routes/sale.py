from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.sale import SaleCreate, SaleResponse, SaleUpdate
from app.models.sale import Sale, SaleItem, PaymentMethod
from app.models.product import Product
from app.security import get_current_active_user
from app.hardware.printer import get_printer, PrinterError
from app.crud import dayend as dayend_crud
from config import settings
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
        # Fetch product details
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        sale_item = SaleItem(
            sale_id=db_sale.id,
            product_id=item.product_id,
            product_name=product.name,
            product_code=product.code,
            quantity=item.quantity,
            unit_price=item.unit_price,
            discount=item.discount,
            tax=item.tax,
            subtotal=item.unit_price * item.quantity
        )
        db.add(sale_item)
    
    db.commit()
    db.refresh(db_sale)
    
    # Automatically add sale to active dayend for the cashier
    try:
        active_dayend = dayend_crud.get_or_create_active_dayend(db, current_user.id)
        dayend_crud.add_sale_to_dayend(db, active_dayend.id, db_sale.id)
        # Recalculate dayend summary
        dayend_crud.calculate_dayend_summary(db, active_dayend.id)
    except Exception as e:
        # Don't fail the sale if dayend linking fails
        print(f"Warning: Could not link sale to dayend: {str(e)}")
    
    # Open cash drawer if payment method is cash and auto-open is enabled
    auto_open_drawer = getattr(settings, 'AUTO_OPEN_CASH_DRAWER', True)
    open_for_cash_only = getattr(settings, 'OPEN_DRAWER_FOR_CASH_ONLY', True)
    
    should_open_drawer = False
    if auto_open_drawer:
        if open_for_cash_only:
            # Only open for cash payments
            if db_sale.payment_method == PaymentMethod.CASH:
                should_open_drawer = True
        else:
            # Open for all payment methods
            should_open_drawer = True
    
    if should_open_drawer:
        try:
            printer = get_printer()
            # Try to connect if not connected, but don't fail if it doesn't work
            if not printer.is_connected:
                try:
                    printer.connect()
                except PrinterError:
                    # Printer not available, skip drawer opening
                    pass
            
            # Open drawer if printer is connected
            if printer.is_connected:
                try:
                    printer.open_cash_drawer()
                except PrinterError as e:
                    # Log but don't fail the sale if drawer can't open
                    print(f"Warning: Could not open cash drawer: {str(e)}")
        except Exception as e:
            # Don't fail the sale if drawer opening fails
            print(f"Warning: Cash drawer error: {str(e)}")
    
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
