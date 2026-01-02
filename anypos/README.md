# AnyPos - Modern POS System

A modern, scalable Point of Sale (POS) system built with Python and FastAPI, designed for retail businesses. AnyPos is a rebranded version with all the features of Aronium Lite and more.

## Features

### Core Features
- ✅ **User Management** - Multi-role user system (Admin, Manager, Cashier, Staff)
- ✅ **Product Management** - Product catalog with categories, pricing, and stock tracking
- ✅ **Sales Management** - Complete point-of-sale with receipt generation
- ✅ **Customer Management** - Customer database with loyalty points and credit tracking
- ✅ **Inventory Management** - Stock adjustments, low stock alerts
- ✅ **Expense Tracking** - Record business expenses with categories
- ✅ **Reporting & Analytics** - Sales reports, dashboard statistics
- ✅ **Authentication** - Secure JWT-based authentication
- ✅ **Barcode Support** - Barcode scanning for products

## Tech Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Server**: Uvicorn
- **Database**: PostgreSQL / SQLite
- **ORM**: SQLAlchemy
- **Authentication**: JWT (python-jose)
- **Password Hashing**: Bcrypt

### Frontend (To be implemented)
- React / Vue.js
- Tailwind CSS
- Axios for API calls

## Installation

### Prerequisites
- Python 3.9+
- pip or conda
- PostgreSQL (optional, SQLite works for development)

### Setup

1. **Clone the repository**
```bash
git clone <your-repo>
cd anypos
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run the application**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login user
- `POST /api/auth/register` - Register new user

### Products
- `GET /api/products` - List products
- `GET /api/products/{id}` - Get product
- `POST /api/products` - Create product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product
- `GET /api/products/search?q=term` - Search products
- `GET /api/products/categories` - List categories
- `POST /api/products/categories` - Create category
- `GET /api/products/low-stock` - Low stock products

### Sales
- `GET /api/sales` - List sales
- `POST /api/sales` - Create sale
- `GET /api/sales/{id}` - Get sale details
- `PUT /api/sales/{id}` - Update sale
- `DELETE /api/sales/{id}` - Cancel sale

### Customers
- `GET /api/customers` - List customers
- `POST /api/customers` - Create customer
- `GET /api/customers/{id}` - Get customer
- `PUT /api/customers/{id}` - Update customer
- `DELETE /api/customers/{id}` - Delete customer
- `GET /api/customers/search?q=term` - Search customers

### Inventory
- `GET /api/inventory` - List adjustments
- `POST /api/inventory` - Create adjustment

### Expenses
- `GET /api/expenses` - List expenses
- `POST /api/expenses` - Create expense
- `GET /api/expenses/categories` - Expense categories

### Reports
- `GET /api/reports/dashboard` - Dashboard statistics
- `GET /api/reports/sales` - Sales report
- `GET /api/reports/products/top` - Top products

## Database Schema

### Core Tables
- **users** - User accounts and roles
- **products** - Product catalog
- **categories** - Product categories
- **customers** - Customer information
- **sales** - Sales transactions
- **sale_items** - Individual items in sales
- **stock_adjustments** - Inventory adjustments
- **expenses** - Business expenses

## User Roles

- **Admin** - Full system access
- **Manager** - Manager-level permissions
- **Cashier** - Sales and customer operations
- **Staff** - Limited access

## Configuration

Edit `.env` file to configure:
```env
APP_NAME=AnyPos
DATABASE_URL=sqlite:///./anypos.db
SECRET_KEY=your-secret-key
DEBUG=True
HOST=0.0.0.0
PORT=8000
CORS_ORIGINS=http://localhost:3000
```

## Development

### Project Structure
```
anypos/
├── backend/
│   ├── app/
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── routes/       # API endpoints
│   │   ├── crud/         # Database operations
│   │   ├── database.py   # Database setup
│   │   └── security.py   # JWT & Auth
│   ├── main.py           # App entry point
│   └── config.py         # Configuration
├── frontend/             # React/Vue frontend
├── requirements.txt      # Python dependencies
└── .env.example          # Environment template
```

## Roadmap

- [ ] Frontend implementation (React)
- [ ] Advanced reporting
- [ ] Receipt printing
- [ ] Multi-store support
- [ ] Cloud backup
- [ ] Mobile app
- [ ] Payment gateway integration
- [ ] Loyalty program
- [ ] Supplier management

## Contributing

Contributions are welcome! Please follow the code style and add tests for new features.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.

## Credits

Built as a modern Python-based rebranding of Aronium Lite POS system.
