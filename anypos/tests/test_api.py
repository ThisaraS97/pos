"""
AnyPos POS System - Tests
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from main import app
from app.database import Base, engine

client = TestClient(app)

# Setup and teardown
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_health():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "AnyPos" in response.json()["app"]

# Authentication tests
def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post("/api/auth/login", json={
        "username": "nonexistent",
        "password": "wrong"
    })
    assert response.status_code == 401

def test_register_user():
    """Test user registration"""
    response = client.post("/api/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User",
        "role": "staff"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

# Product tests
def test_get_products_empty():
    """Test getting products when none exist"""
    response = client.get("/api/products")
    assert response.status_code == 200
    assert response.json() == []

# Run tests with: pytest tests/
