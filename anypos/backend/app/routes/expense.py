from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import datetime
from app.database import get_db
from app.models.expense import Expense, ExpenseCategory
from app.security import get_current_active_user

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])

class ExpenseCategoryCreate(BaseModel):
    name: str
    description: str = ""

class ExpenseCreate(BaseModel):
    category_id: int
    description: str
    amount: float
    reference: str = ""

class ExpenseResponse(BaseModel):
    id: int
    category_id: int
    description: str
    amount: float
    reference: str
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/categories", response_model=List[BaseModel])
def get_expense_categories(db: Session = Depends(get_db)):
    """Get expense categories"""
    return db.query(ExpenseCategory).all()

@router.post("/categories", response_model=BaseModel)
def create_expense_category(category: ExpenseCategoryCreate, db: Session = Depends(get_db),
                           current_user = Depends(get_current_active_user)):
    """Create expense category"""
    db_category = ExpenseCategory(name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.get("", response_model=List[ExpenseResponse])
def get_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get expenses"""
    return db.query(Expense).offset(skip).limit(limit).all()

@router.post("", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db),
                  current_user = Depends(get_current_active_user)):
    """Create an expense"""
    db_expense = Expense(
        category_id=expense.category_id,
        description=expense.description,
        amount=expense.amount,
        reference=expense.reference,
        recorded_by=current_user.id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense
