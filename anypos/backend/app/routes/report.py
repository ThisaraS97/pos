from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.sale import Sale
from app.models.product import Product
from app.models.customer import Customer
from app.security import get_current_active_user
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db),
                       current_user = Depends(get_current_active_user)):
    """Get dashboard statistics"""
    today = datetime.now().date()
    start_of_month = datetime.now().replace(day=1).date()
    start_of_year = datetime.now().replace(month=1, day=1).date()
    
    # Today's sales
    today_sales = db.query(Sale).filter(
        func.date(Sale.created_at) == today,
        Sale.is_deleted == False
    ).all()
    
    today_revenue = sum(s.total for s in today_sales) if today_sales else 0
    
    # Month's sales
    month_sales = db.query(Sale).filter(
        func.date(Sale.created_at) >= start_of_month,
        Sale.is_deleted == False
    ).all()
    
    month_revenue = sum(s.total for s in month_sales) if month_sales else 0
    
    # Year's sales
    year_sales = db.query(Sale).filter(
        func.date(Sale.created_at) >= start_of_year,
        Sale.is_deleted == False
    ).all()
    
    year_revenue = sum(s.total for s in year_sales) if year_sales else 0
    
    # Count stats
    total_products = db.query(Product).filter(Product.is_active == True).count()
    total_customers = db.query(Customer).filter(Customer.is_active == True).count()
    
    return {
        "today_sales": len(today_sales),
        "today_revenue": today_revenue,
        "month_sales": len(month_sales),
        "month_revenue": month_revenue,
        "year_revenue": year_revenue,
        "total_products": total_products,
        "total_customers": total_customers
    }

@router.get("/sales")
def get_sales_report(start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    """Get sales report"""
    query = db.query(Sale).filter(Sale.is_deleted == False)
    
    if start_date:
        query = query.filter(func.date(Sale.created_at) >= start_date)
    if end_date:
        query = query.filter(func.date(Sale.created_at) <= end_date)
    
    sales = query.all()
    return {
        "total_sales": len(sales),
        "total_revenue": sum(s.total for s in sales) if sales else 0,
        "average_sale": sum(s.total for s in sales) / len(sales) if sales else 0
    }

@router.get("/products/top")
def get_top_products(limit: int = 10, db: Session = Depends(get_db)):
    """Get top selling products"""
    from app.models.sale import SaleItem
    
    # Get top selling products
    top_products = db.query(
        Product.id,
        Product.name,
        Product.code,
        func.sum(SaleItem.quantity).label('total_quantity'),
        func.sum(SaleItem.subtotal).label('total_revenue')
    ).join(
        SaleItem, SaleItem.product_id == Product.id
    ).filter(
        Product.is_active == True
    ).group_by(
        Product.id, Product.name, Product.code
    ).order_by(
        func.sum(SaleItem.quantity).desc()
    ).limit(limit).all()
    
    return [
        {
            "id": p[0],
            "name": p[1],
            "code": p[2],
            "units_sold": int(p[3]) if p[3] else 0,
            "total_revenue": float(p[4]) if p[4] else 0.0,
            "avg_price": float(p[4] / p[3]) if p[3] and p[4] else 0.0
        }
        for p in top_products
    ]
