from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.dayend import DayEnd, DayEndTransaction
from app.models.sale import Sale
from app.security import get_current_active_user
from app.schemas.dayend import (
    DayEndCreate, DayEndClose, DayEndResponse, 
    DayEndList, DayEndSummary
)
from app.crud import dayend as dayend_crud
from datetime import datetime, date

router = APIRouter(prefix="/api/dayend", tags=["Day End"])


@router.post("/open", response_model=DayEndResponse)
def open_dayend(
    dayend_data: DayEndCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Open/Get active day-end for current cashier"""
    # Get or create active dayend
    dayend = dayend_crud.get_or_create_active_dayend(db, current_user.id)
    
    # Update opening balance if provided
    if dayend_data.opening_balance:
        dayend.opening_balance = dayend_data.opening_balance
    
    if dayend_data.notes:
        dayend.notes = dayend_data.notes
    
    db.commit()
    db.refresh(dayend)
    
    return dayend


@router.get("/active", response_model=DayEndResponse)
def get_active_dayend(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get active day-end for current cashier"""
    today = date.today()
    
    dayend = db.query(DayEnd).filter(
        DayEnd.cashier_id == current_user.id,
        DayEnd.is_closed == False,
        func.date(DayEnd.opened_at) == today
    ).first()
    
    if not dayend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active day-end found. Please open a day-end first."
        )
    
    return dayend


@router.get("/list")
def list_dayends(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List all day-ends"""
    # Only admins and managers can view all day-ends
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view day-ends list"
        )
    
    dayends = dayend_crud.list_dayends(db, skip, limit)
    
    return [
        {
            "id": d.id,
            "cashier_id": d.cashier_id,
            "opened_at": d.opened_at,
            "closed_at": d.closed_at,
            "is_closed": d.is_closed,
            "total_revenue": d.total_revenue,
            "total_sales_count": d.total_sales_count,
            "cash_variance": d.cash_variance
        }
        for d in dayends
    ]


@router.get("/{dayend_id}", response_model=DayEndResponse)
def get_dayend(
    dayend_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get day-end by ID"""
    dayend = dayend_crud.get_dayend_by_id(db, dayend_id)
    
    if not dayend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Day-end not found"
        )
    
    # Check authorization (admin can view all, cashier can only view their own)
    if current_user.role != "admin" and dayend.cashier_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this day-end"
        )
    
    return dayend


@router.get("/{dayend_id}/summary", response_model=DayEndSummary)
def get_dayend_summary(
    dayend_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get formatted day-end summary report"""
    dayend = dayend_crud.get_dayend_by_id(db, dayend_id)
    
    if not dayend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Day-end not found"
        )
    
    # Check authorization
    if current_user.role != "admin" and dayend.cashier_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this day-end"
        )
    
    summary = dayend_crud.get_dayend_summary_report(db, dayend_id)
    return summary


@router.post("/{dayend_id}/add-sale/{sale_id}")
def add_sale_to_dayend(
    dayend_id: int,
    sale_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Add a sale to the day-end"""
    dayend = dayend_crud.get_dayend_by_id(db, dayend_id)
    
    if not dayend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Day-end not found"
        )
    
    if dayend.is_closed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add sales to a closed day-end"
        )
    
    # Check authorization
    if current_user.role != "admin" and dayend.cashier_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this day-end"
        )
    
    # Verify sale exists
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )
    
    transaction = dayend_crud.add_sale_to_dayend(db, dayend_id, sale_id)
    
    # Recalculate summary
    dayend = dayend_crud.calculate_dayend_summary(db, dayend_id)
    
    return {
        "message": "Sale added to day-end",
        "dayend": dayend
    }


@router.post("/{dayend_id}/close", response_model=DayEndResponse)
def close_dayend(
    dayend_id: int,
    close_data: DayEndClose,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Close the day-end"""
    dayend = dayend_crud.get_dayend_by_id(db, dayend_id)
    
    if not dayend:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Day-end not found"
        )
    
    if dayend.is_closed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Day-end is already closed"
        )
    
    # Check authorization
    if current_user.role != "admin" and dayend.cashier_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to close this day-end"
        )
    
    closed_dayend = dayend_crud.close_dayend(
        db, dayend_id, 
        close_data.actual_cash, 
        close_data.notes
    )
    
    return closed_dayend


@router.get("/cashier/{cashier_id}/history")
def get_cashier_dayend_history(
    cashier_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get day-end history for a specific cashier"""
    # Check authorization
    if current_user.role != "admin" and current_user.id != cashier_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this history"
        )
    
    dayends = db.query(DayEnd).filter(
        DayEnd.cashier_id == cashier_id
    ).order_by(
        DayEnd.opened_at.desc()
    ).offset(skip).limit(limit).all()
    
    return [
        {
            "id": d.id,
            "opened_at": d.opened_at,
            "closed_at": d.closed_at,
            "is_closed": d.is_closed,
            "total_revenue": d.total_revenue,
            "total_sales_count": d.total_sales_count,
            "cash_variance": d.cash_variance
        }
        for d in dayends
    ]
