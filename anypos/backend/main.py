from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from app.database import Base, engine
from app.routes import auth, product, sale, customer, inventory, expense, report
from app.models import *

# Create tables
Base.metadata.create_all(bind=engine)

def create_app():
    app = FastAPI(
        title=settings.APP_NAME,
        description="Modern POS System",
        version="1.0.0"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(auth.router)
    app.include_router(product.router)
    app.include_router(sale.router)
    app.include_router(customer.router)
    app.include_router(inventory.router)
    app.include_router(expense.router)
    app.include_router(report.router)
    
    @app.get("/")
    def read_root():
        return {
            "app": settings.APP_NAME,
            "version": "1.0.0",
            "status": "running"
        }
    
    @app.get("/health")
    def health_check():
        return {"status": "healthy"}
    
    return app

app = create_app()
