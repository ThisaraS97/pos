#!/usr/bin/env python
"""
Initialize AnyPos database with sample data
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.database import SessionLocal, Base, engine
from app.crud.user import create_user
from app.crud.product import create_category, create_product
from app.crud.customer import create_customer
from app.schemas.user import UserCreate, UserRole
from app.schemas.product import CategoryCreate, ProductCreate
from pydantic import BaseModel

# Create all tables first
print("🗄️  Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created!")

db = SessionLocal()

print("🚀 Initializing AnyPos Database...")

# Create users
print("\n📝 Creating users...")
users_data = [
    {"username": "admin", "email": "admin@anypos.com", "password": "admin123", "full_name": "Admin User", "role": UserRole.ADMIN},
    {"username": "manager", "email": "manager@anypos.com", "password": "manager123", "full_name": "Manager User", "role": UserRole.MANAGER},
    {"username": "cashier", "email": "cashier@anypos.com", "password": "cashier123", "full_name": "Cashier User", "role": UserRole.CASHIER},
]

for user_data in users_data:
    try:
        user = create_user(db, UserCreate(**user_data))
        print(f"  ✓ Created user: {user.username}")
    except Exception as e:
        db.rollback()
        print(f"  ✗ Error creating {user_data['username']}: {e}")

# Create categories
print("\n📂 Creating product categories...")
categories_data = [
    {"name": "Electronics", "description": "Electronic items"},
    {"name": "Clothing", "description": "Clothing and apparel"},
    {"name": "Food", "description": "Food and beverages"},
    {"name": "Books", "description": "Books and publications"},
    {"name": "Home", "description": "Home and garden"},
]

categories = {}
for cat_data in categories_data:
    try:
        category = create_category(db, CategoryCreate(**cat_data))
        categories[cat_data["name"]] = category.id
        print(f"  ✓ Created category: {category.name}")
    except Exception as e:
        print(f"  ✗ Error creating category: {e}")

# Create products
print("\n📦 Creating products...")
products_data = [
    {"code": "ELEC001", "name": "Laptop", "category_id": categories.get("Electronics"), "cost_price": 400, "selling_price": 599, "quantity_in_stock": 10, "barcode": "5901234123457"},
    {"code": "ELEC002", "name": "Mouse", "category_id": categories.get("Electronics"), "cost_price": 5, "selling_price": 12.99, "quantity_in_stock": 50},
    {"code": "ELEC003", "name": "Keyboard", "category_id": categories.get("Electronics"), "cost_price": 15, "selling_price": 39.99, "quantity_in_stock": 30},
    {"code": "CLTH001", "name": "T-Shirt", "category_id": categories.get("Clothing"), "cost_price": 5, "selling_price": 14.99, "quantity_in_stock": 100},
    {"code": "CLTH002", "name": "Jeans", "category_id": categories.get("Clothing"), "cost_price": 20, "selling_price": 49.99, "quantity_in_stock": 40},
    {"code": "FOOD001", "name": "Coffee", "category_id": categories.get("Food"), "cost_price": 2, "selling_price": 4.99, "quantity_in_stock": 200},
    {"code": "FOOD002", "name": "Tea", "category_id": categories.get("Food"), "cost_price": 1, "selling_price": 3.99, "quantity_in_stock": 150},
    {"code": "BOOK001", "name": "Python Programming", "category_id": categories.get("Books"), "cost_price": 30, "selling_price": 59.99, "quantity_in_stock": 20},
    {"code": "HOME001", "name": "Pillow", "category_id": categories.get("Home"), "cost_price": 10, "selling_price": 24.99, "quantity_in_stock": 50},
    {"code": "HOME002", "name": "Blanket", "category_id": categories.get("Home"), "cost_price": 15, "selling_price": 39.99, "quantity_in_stock": 30},
]

for prod_data in products_data:
    try:
        product = create_product(db, ProductCreate(**prod_data))
        print(f"  ✓ Created product: {product.name}")
    except Exception as e:
        print(f"  ✗ Error creating product: {e}")

# Create customers
print("\n👥 Creating customers...")
customers_data = [
    {"name": "John Doe", "phone": "555-0001", "email": "john@example.com", "address": "123 Main St", "city": "New York"},
    {"name": "Jane Smith", "phone": "555-0002", "email": "jane@example.com", "address": "456 Oak Ave", "city": "Boston"},
    {"name": "Bob Johnson", "phone": "555-0003", "email": "bob@example.com", "address": "789 Pine Rd", "city": "Chicago"},
]

class CustomerCreateSchema(BaseModel):
    name: str
    phone: str
    email: str
    address: str
    city: str

for cust_data in customers_data:
    try:
        customer = create_customer(db, CustomerCreateSchema(**cust_data))
        print(f"  ✓ Created customer: {customer.name}")
    except Exception as e:
        print(f"  ✗ Error creating customer: {e}")

print("\n✅ Database initialization completed!")
print("\n📋 Login credentials:")
for user in users_data:
    print(f"  - {user['username']} / {user['password']}")
