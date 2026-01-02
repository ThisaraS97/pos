# AnyPos Quick Start Guide

## 🚀 Quick Start (5 minutes)

### Windows

1. **Download & Extract**
   - Extract the AnyPos project folder

2. **Run Startup Script**
   ```bash
   cd anypos
   scripts\startup.bat
   ```

3. **Access the system**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Frontend: http://localhost:3000 (after setting up frontend)

### Linux/Mac

1. **Download & Extract**
   ```bash
   cd anypos
   ```

2. **Run Startup Script**
   ```bash
   chmod +x scripts/startup.sh
   ./scripts/startup.sh
   ```

3. **Access the system**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🐳 Docker Setup

### Prerequisites
- Docker and Docker Compose installed

### Run with Docker

```bash
docker-compose up -d
```

Access:
- API: http://localhost:8000
- Database: postgres://localhost:5432/anypos

### Shutdown

```bash
docker-compose down
```

## 🔐 Default Login Credentials

After running the initialization script:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| manager | manager123 | Manager |
| cashier | cashier123 | Cashier |

## 📊 API Testing

### Using Swagger UI
Visit: http://localhost:8000/docs

### Using curl

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Copy the access_token from response

# Get products (replace TOKEN with actual token)
curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/products
```

## 🔧 Configuration

Edit the `.env` file to customize:

```env
APP_NAME=AnyPos
DATABASE_URL=sqlite:///./anypos.db  # or postgresql://...
SECRET_KEY=your-secret-key
DEBUG=True
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000
COMPANY_NAME=AnyPos
COMPANY_ADDRESS=Your Address
COMPANY_PHONE=Your Phone
COMPANY_EMAIL=Your Email
```

## 📱 Available Features

### Sales
- Create sales transactions
- Add items to cart
- Apply discounts
- Track payment methods
- Generate receipts

### Products
- Add/Edit/Delete products
- Product categories
- Barcode scanning
- Stock tracking
- Low stock alerts

### Customers
- Customer database
- Loyalty points
- Credit tracking
- Customer search

### Inventory
- Stock adjustments
- Stock history
- Low stock reports
- Product movements

### Reports
- Dashboard statistics
- Sales analytics
- Product reports
- Expense tracking

### Users
- Multi-user support
- Role-based access control
- User authentication
- Activity tracking

## 🛠️ Development

### Install for Development

```bash
cd anypos

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run with auto-reload
cd backend
uvicorn main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

## 📚 Documentation

- **Backend**: See [README.md](README.md)
- **Development**: See [DEVELOPMENT.md](DEVELOPMENT.md)
- **API**: See http://localhost:8000/docs when running

## 🐛 Troubleshooting

### Port 8000 Already in Use

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -i :8000
kill -9 <PID>
```

### Database Issues

- Delete `anypos.db` and restart for fresh database
- For PostgreSQL, ensure database is created and running

### CORS Issues

- Update `CORS_ORIGINS` in `.env` with your frontend URL

## 📞 Support

For issues and questions:
1. Check [DEVELOPMENT.md](DEVELOPMENT.md)
2. Review API Documentation at http://localhost:8000/docs
3. Check logs in terminal

## 🚀 Next Steps

1. **Customize branding** - Update company info in `.env`
2. **Create admin user** - Use the init script or API
3. **Add products** - Create product categories and items
4. **Setup customers** - Add customer database
5. **Configure receipts** - Customize receipt format
6. **Deploy** - Use Docker or your preferred hosting

## 📄 License

MIT License - See LICENSE file for details
