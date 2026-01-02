from sqlalchemy.orm import Session
from app.models.customer import Customer

def get_customer(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id, Customer.is_active == True).first()

def get_customer_by_phone(db: Session, phone: str):
    return db.query(Customer).filter(Customer.phone == phone, Customer.is_active == True).first()

def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email, Customer.is_active == True).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Customer).filter(Customer.is_active == True).offset(skip).limit(limit).all()

def search_customers(db: Session, search_term: str):
    return db.query(Customer).filter(
        Customer.is_active == True,
        (Customer.name.ilike(f"%{search_term}%") | 
         Customer.phone.ilike(f"%{search_term}%") |
         Customer.email.ilike(f"%{search_term}%"))
    ).all()

def create_customer(db: Session, customer_data):
    db_customer = Customer(**customer_data.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def update_customer(db: Session, customer_id: int, customer_update):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        update_data = customer_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_customer, field, value)
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
    return db_customer

def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer(db, customer_id)
    if db_customer:
        db_customer.is_active = False
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
    return db_customer
