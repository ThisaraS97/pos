# AnyPos Development Guide

## Backend Setup

### 1. Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
cd backend
pip install -r ../requirements.txt
```

### 3. Database Setup
For development with SQLite (default):
- No setup needed, database will be created automatically

For PostgreSQL:
```bash
# Update DATABASE_URL in .env
# Create database
createdb anypos
```

### 4. Run Backend
```bash
cd backend
uvicorn main:app --reload
```

## Frontend Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Development Server
```bash
npm run dev
```

## Testing API

### Using curl
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'

# Get products
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/products
```

### Using Python requests
```python
import requests

API_URL = "http://localhost:8000/api"

# Login
response = requests.post(f"{API_URL}/auth/login", json={
    "username": "admin",
    "password": "password"
})
token = response.json()["access_token"]

# Get products
headers = {"Authorization": f"Bearer {token}"}
products = requests.get(f"{API_URL}/products", headers=headers).json()
```

## Creating Initial Data

After starting the application, you can create initial data through the API or using the following script:

```python
# scripts/init_data.py
from app.database import SessionLocal
from app.crud.user import create_user
from app.schemas.user import UserCreate, UserRole

db = SessionLocal()

# Create admin user
admin = create_user(db, UserCreate(
    username="admin",
    email="admin@anypos.local",
    password="admin123",
    role=UserRole.ADMIN
))

# Create cashier user
cashier = create_user(db, UserCreate(
    username="cashier",
    email="cashier@anypos.local",
    password="cashier123",
    role=UserRole.CASHIER
))

print("Initial data created!")
```

## Common Issues

### Port Already in Use
```bash
# Linux/Mac
lsof -i :8000
kill -9 <PID>

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Database Locked
Delete `anypos.db` and restart

### CORS Issues
Update `CORS_ORIGINS` in `.env`

## Database Migrations

When models change, tables are automatically created/updated on application start due to `Base.metadata.create_all()`.

For production, consider using Alembic for proper migrations:
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```
