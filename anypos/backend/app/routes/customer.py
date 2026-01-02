from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.models.customer import Customer
from app.security import get_current_active_user
from app.crud.customer import (
    get_customer, create_customer, get_customers, update_customer, 
    delete_customer, search_customers
)

router = APIRouter(prefix="/api/customers", tags=["Customers"])

class CustomerCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    notes: Optional[str] = None

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    notes: Optional[str] = None

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    loyalty_points: float
    balance: float

    class Config:
        from_attributes = True

@router.get("", response_model=List[CustomerResponse])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all customers"""
    return get_customers(db, skip, limit)

@router.get("/search", response_model=List[CustomerResponse])
def search_customers_endpoint(q: str, db: Session = Depends(get_db)):
    """Search customers"""
    return search_customers(db, q)

@router.post("", response_model=CustomerResponse)
def create_customer_endpoint(customer: CustomerCreate, db: Session = Depends(get_db),
                            current_user = Depends(get_current_active_user)):
    """Create a new customer"""
    return create_customer(db, customer)

@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer_endpoint(customer_id: int, db: Session = Depends(get_db)):
    """Get a customer by ID"""
    customer = get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=CustomerResponse)
def update_customer_endpoint(customer_id: int, customer_update: CustomerUpdate,
                            db: Session = Depends(get_db),
                            current_user = Depends(get_current_active_user)):
    """Update a customer"""
    customer = update_customer(db, customer_id, customer_update)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.delete("/{customer_id}")
def delete_customer_endpoint(customer_id: int, db: Session = Depends(get_db),
                            current_user = Depends(get_current_active_user)):
    """Delete a customer"""
    customer = delete_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"message": "Customer deleted"}
