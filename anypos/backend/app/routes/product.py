from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.product import CategoryCreate, CategoryResponse, ProductCreate, ProductResponse, ProductUpdate
from app.crud.product import (
    get_category, create_category, get_categories, delete_category,
    get_product, create_product, get_products, update_product, delete_product,
    get_product_by_code, get_product_by_barcode, search_products, get_low_stock_products
)
from app.security import get_current_active_user

router = APIRouter(prefix="/api/products", tags=["Products"])

# Category endpoints
@router.get("/categories", response_model=List[CategoryResponse])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all categories"""
    return get_categories(db, skip, limit)

@router.post("/categories", response_model=CategoryResponse)
def create_category_endpoint(category: CategoryCreate, db: Session = Depends(get_db), 
                            current_user = Depends(get_current_active_user)):
    """Create a new category"""
    return create_category(db, category)

@router.delete("/categories/{category_id}")
def delete_category_endpoint(category_id: int, db: Session = Depends(get_db),
                            current_user = Depends(get_current_active_user)):
    """Delete a category"""
    category = delete_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted"}

# Product endpoints
@router.get("", response_model=List[ProductResponse])
def list_products(skip: int = 0, limit: int = 100, category_id: int = None, 
                 db: Session = Depends(get_db)):
    """Get all products"""
    return get_products(db, skip, limit, category_id)

@router.get("/search", response_model=List[ProductResponse])
def search_products_endpoint(q: str, skip: int = 0, limit: int = 100,
                            db: Session = Depends(get_db)):
    """Search products by name, code, or barcode"""
    return search_products(db, q, skip, limit)

@router.get("/low-stock", response_model=List[ProductResponse])
def get_low_stock_products_endpoint(db: Session = Depends(get_db)):
    """Get products with low stock"""
    return get_low_stock_products(db)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    """Get a product by ID"""
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("", response_model=ProductResponse)
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db),
                           current_user = Depends(get_current_active_user)):
    """Create a new product"""
    existing = get_product_by_code(db, product.code)
    if existing:
        raise HTTPException(status_code=400, detail="Product code already exists")
    return create_product(db, product)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product_endpoint(product_id: int, product_update: ProductUpdate, 
                           db: Session = Depends(get_db),
                           current_user = Depends(get_current_active_user)):
    """Update a product"""
    product = update_product(db, product_id, product_update)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db),
                           current_user = Depends(get_current_active_user)):
    """Delete a product"""
    product = delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}
