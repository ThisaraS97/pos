from sqlalchemy.orm import Session
from app.models.product import Product, Category
from app.schemas.product import ProductCreate, ProductUpdate

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def get_category_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()

def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Category).filter(Category.is_active == True).offset(skip).limit(limit).all()

def create_category(db: Session, category):
    db_category = Category(name=category.name, description=category.description)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category(db, category_id)
    if db_category:
        db_category.is_active = False
        db.add(db_category)
        db.commit()
    return db_category

# Product CRUD
def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()

def get_product_by_code(db: Session, code: str):
    return db.query(Product).filter(Product.code == code, Product.is_active == True).first()

def get_product_by_barcode(db: Session, barcode: str):
    return db.query(Product).filter(Product.barcode == barcode, Product.is_active == True).first()

def get_products(db: Session, skip: int = 0, limit: int = 100, category_id: int = None):
    query = db.query(Product).filter(Product.is_active == True)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    return query.offset(skip).limit(limit).all()

def search_products(db: Session, search_term: str, skip: int = 0, limit: int = 100):
    return db.query(Product).filter(
        Product.is_active == True,
        (Product.name.ilike(f"%{search_term}%") | 
         Product.code.ilike(f"%{search_term}%") |
         Product.barcode.ilike(f"%{search_term}%"))
    ).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: ProductUpdate):
    db_product = get_product(db, product_id)
    if db_product:
        update_data = product_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if db_product:
        db_product.is_active = False
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
    return db_product

def update_product_stock(db: Session, product_id: int, quantity_change: int):
    db_product = get_product(db, product_id)
    if db_product:
        db_product.quantity_in_stock += quantity_change
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
    return db_product

def get_low_stock_products(db: Session):
    return db.query(Product).filter(
        Product.is_active == True,
        Product.quantity_in_stock <= Product.minimum_stock
    ).all()
