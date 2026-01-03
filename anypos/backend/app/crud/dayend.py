from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.dayend import DayEnd, DayEndTransaction
from app.models.sale import Sale, PaymentMethod
from datetime import datetime, date

def get_or_create_active_dayend(db: Session, cashier_id: int):
    """Get active day-end or create a new one"""
    today = date.today()
    
    # Check if there's an unclosed day-end for today
    active_dayend = db.query(DayEnd).filter(
        DayEnd.cashier_id == cashier_id,
        DayEnd.is_closed == False,
        func.date(DayEnd.opened_at) == today
    ).first()
    
    if not active_dayend:
        # Create new day-end
        active_dayend = DayEnd(
            cashier_id=cashier_id,
            opening_balance=0.0
        )
        db.add(active_dayend)
        db.commit()
        db.refresh(active_dayend)
    
    return active_dayend


def get_dayend_by_id(db: Session, dayend_id: int):
    """Get day-end by ID"""
    return db.query(DayEnd).filter(DayEnd.id == dayend_id).first()


def list_dayends(db: Session, skip: int = 0, limit: int = 100):
    """List all day-ends with pagination"""
    return db.query(DayEnd).order_by(DayEnd.opened_at.desc()).offset(skip).limit(limit).all()


def calculate_dayend_summary(db: Session, dayend_id: int):
    """Calculate summary for a day-end"""
    dayend = get_dayend_by_id(db, dayend_id)
    
    if not dayend:
        return None
    
    # Get all sales for this day-end
    dayend_transactions = db.query(DayEndTransaction).filter(
        DayEndTransaction.dayend_id == dayend_id
    ).all()
    
    sale_ids = [dt.sale_id for dt in dayend_transactions]
    
    if not sale_ids:
        return dayend
    
    sales = db.query(Sale).filter(Sale.id.in_(sale_ids)).all()
    
    # Calculate totals
    total_sales_count = len(sales)
    total_revenue = sum(s.total for s in sales)
    total_discount = sum(s.discount for s in sales)
    total_tax = sum(s.tax for s in sales)
    
    # Calculate by payment method
    cash_sales = sum(s.total for s in sales if s.payment_method == PaymentMethod.CASH)
    card_sales = sum(s.total for s in sales if s.payment_method == PaymentMethod.CARD)
    cheque_sales = sum(s.total for s in sales if s.payment_method == PaymentMethod.CHEQUE)
    online_sales = sum(s.total for s in sales if s.payment_method == PaymentMethod.ONLINE)
    credit_sales = sum(s.total for s in sales if s.payment_method == PaymentMethod.CREDIT)
    
    # Update dayend
    dayend.total_sales_count = total_sales_count
    dayend.total_revenue = total_revenue
    dayend.total_discount = total_discount
    dayend.total_tax = total_tax
    dayend.cash_sales = cash_sales
    dayend.card_sales = card_sales
    dayend.cheque_sales = cheque_sales
    dayend.online_sales = online_sales
    dayend.credit_sales = credit_sales
    dayend.expected_cash = cash_sales
    dayend.cash_variance = dayend.actual_cash - dayend.expected_cash
    
    db.commit()
    db.refresh(dayend)
    
    return dayend


def add_sale_to_dayend(db: Session, dayend_id: int, sale_id: int):
    """Add a sale to day-end"""
    # Check if already added
    existing = db.query(DayEndTransaction).filter(
        DayEndTransaction.dayend_id == dayend_id,
        DayEndTransaction.sale_id == sale_id
    ).first()
    
    if existing:
        return existing
    
    transaction = DayEndTransaction(
        dayend_id=dayend_id,
        sale_id=sale_id
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    
    return transaction


def close_dayend(db: Session, dayend_id: int, actual_cash: float, notes: str = None):
    """Close the day-end"""
    dayend = get_dayend_by_id(db, dayend_id)
    
    if not dayend:
        return None
    
    if dayend.is_closed:
        return dayend  # Already closed
    
    # Calculate summary first
    calculate_dayend_summary(db, dayend_id)
    
    # Update with final values
    dayend.actual_cash = actual_cash
    dayend.cash_variance = dayend.actual_cash - dayend.expected_cash
    dayend.closing_balance = dayend.opening_balance + dayend.total_revenue
    dayend.notes = notes
    dayend.is_closed = True
    dayend.closed_at = datetime.now()
    
    db.commit()
    db.refresh(dayend)
    
    return dayend


def get_dayend_summary_report(db: Session, dayend_id: int):
    """Get a formatted day-end summary report"""
    dayend = get_dayend_by_id(db, dayend_id)
    
    if not dayend:
        return None
    
    return {
        "id": dayend.id,
        "cashier_id": dayend.cashier_id,
        "opened_at": dayend.opened_at,
        "closed_at": dayend.closed_at,
        "is_closed": dayend.is_closed,
        "sales_summary": {
            "total_sales": dayend.total_sales_count,
            "total_revenue": dayend.total_revenue,
            "total_discount": dayend.total_discount,
            "total_tax": dayend.total_tax
        },
        "payment_breakdown": {
            "cash": dayend.cash_sales,
            "card": dayend.card_sales,
            "cheque": dayend.cheque_sales,
            "online": dayend.online_sales,
            "credit": dayend.credit_sales
        },
        "cash_reconciliation": {
            "opening_balance": dayend.opening_balance,
            "expected_cash": dayend.expected_cash,
            "actual_cash": dayend.actual_cash,
            "variance": dayend.cash_variance,
            "closing_balance": dayend.closing_balance
        },
        "notes": dayend.notes
    }
