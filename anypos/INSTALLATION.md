# AnyPos Installation & Deployment Guide

## System Requirements

### Minimum Requirements
- Python 3.9+
- 2GB RAM
- 1GB Storage
- Windows/macOS/Linux

### Recommended Requirements
- Python 3.11+
- 4GB RAM
- 5GB Storage
- PostgreSQL 13+
- Modern web browser

## Installation Methods

## Method 1: Quick Start (Windows/Mac/Linux)

### Step 1: Extract Project
```bash
# Extract the anypos.zip file
cd anypos
```

### Step 2: Run Startup Script

**Windows:**
```bash
scripts\startup.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/startup.sh
./scripts/startup.sh
```

### Step 3: Wait for Server
- Backend will start on http://localhost:8000
- Database will be initialized
- Sample data will be created

### Step 4: Access the System
- Open http://localhost:8000 in browser
- Or http://localhost:8000/docs for API documentation
- Login with admin/admin123

---

## Method 2: Manual Installation

### Step 1: Setup Python Environment

**Windows:**
```bash
cd anypos
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
cd anypos
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Configure Environment
```bash
cp .env.example .env
# Edit .env as needed
```

### Step 4: Initialize Database
```bash
cd backend
# On Linux/Mac, ensure you're in the project root for imports
python ../scripts/init_data.py
```

### Step 5: Start Backend
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 6: Access API
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Swagger UI: http://localhost:8000/swagger/index.html

---

## Method 3: Docker Installation

### Prerequisites
- Docker installed ([Download Docker](https://www.docker.com/download))
- Docker Compose installed

### Step 1: Build and Run

```bash
cd anypos
docker-compose up -d
```

### Step 2: Initialize Database
```bash
docker-compose exec backend python scripts/init_data.py
```

### Step 3: Access System
- API: http://localhost:8000
- Database: postgres://anypos:anypos_password@localhost:5432/anypos

### Useful Docker Commands

```bash
# View logs
docker-compose logs -f backend

# Stop containers
docker-compose down

# Remove all data
docker-compose down -v

# Rebuild image
docker-compose build --no-cache
```

---

## Method 4: Production Deployment

### Using Gunicorn (Recommended)

#### Install Gunicorn
```bash
pip install gunicorn
```

#### Run with Gunicorn
```bash
cd backend
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Using Docker in Production

#### Build Production Image
```bash
docker build -t anypos:latest .
```

#### Run Production Container
```bash
docker run -d \
  --name anypos-prod \
  -e DATABASE_URL=postgresql://user:pass@db:5432/anypos \
  -e SECRET_KEY=your-secure-key \
  -e DEBUG=False \
  -p 8000:8000 \
  anypos:latest
```

### Using Nginx (Reverse Proxy)

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Using AWS/Cloud Platforms

#### AWS EC2
```bash
# 1. Launch EC2 instance with Ubuntu 20.04+
# 2. SSH into instance
# 3. Run:
sudo apt-get update
sudo apt-get install python3.11 python3-pip python3-venv postgresql
git clone <your-repo>
cd anypos
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Configure .env with RDS database
python scripts/init_data.py
# Run with gunicorn or docker
```

#### Heroku
```bash
# 1. Install Heroku CLI
# 2. Create Procfile:
echo "web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:\$PORT main:app" > Procfile

# 3. Deploy:
heroku create anypos-app
heroku config:set SECRET_KEY=your-secret-key
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

---

## PostgreSQL Setup

### Local PostgreSQL Installation

**Windows:**
1. Download from https://www.postgresql.org/download/windows/
2. Run installer
3. Note the port (default 5432) and password

**macOS:**
```bash
brew install postgresql
brew services start postgresql
createdb anypos
```

**Linux (Ubuntu):**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
sudo -u postgres createdb anypos
```

### Configure in .env
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/anypos
```

---

## Troubleshooting

### Python Not Found
```bash
# Ensure Python is installed
python --version
# or
python3 --version

# Add to PATH if needed (Windows)
```

### Port Already in Use

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

### Module Not Found
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Database Connection Error

```bash
# Check if PostgreSQL is running
# Windows: Services check PostgreSQL
# Linux: sudo systemctl status postgresql
# Mac: brew services list

# Test connection:
psql -U postgres -d anypos
```

### Permission Denied (Linux/Mac)

```bash
chmod +x scripts/startup.sh
chmod +x backend/main.py
```

---

## Post-Installation Setup

### 1. Change Admin Password
```bash
# Through API or web interface
PUT /api/users/{id}
{
  "password": "your-new-secure-password"
}
```

### 2. Configure Company Info
Edit `.env`:
```env
COMPANY_NAME=Your Company
COMPANY_ADDRESS=123 Main St
COMPANY_PHONE=555-0000
COMPANY_EMAIL=admin@company.com
COMPANY_TAX_ID=12-3456789
```

### 3. Setup Products
- Add product categories
- Add products
- Configure barcode scanner

### 4. Setup Users
- Create manager accounts
- Create cashier accounts
- Assign roles and permissions

### 5. Configure Backup
```bash
# Setup database backups
pg_dump anypos > backup_$(date +%Y%m%d).sql
```

---

## Upgrading AnyPos

### Backup First
```bash
# PostgreSQL backup
pg_dump anypos > backup.sql

# SQLite backup
cp anypos.db anypos.db.backup
```

### Update Code
```bash
git pull origin main
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Database Migration
```bash
# Tables are auto-created, but for schema changes:
python scripts/init_data.py
```

### Restart Application
```bash
# Stop current instance
# Kill the process or use docker-compose down
# Restart with your method
```

---

## Security Hardening

### Essential Security Steps

1. **Change Secret Key**
```env
SECRET_KEY=your-very-long-random-secret-key-min-32-chars
```

2. **Set DEBUG=False in Production**
```env
DEBUG=False
```

3. **Use HTTPS**
- Get SSL certificate (Let's Encrypt free)
- Configure reverse proxy (Nginx)

4. **Strong Database Password**
```
POSTGRES_PASSWORD=complex-random-password-20-chars
```

5. **Firewall Rules**
- Only expose port 80 (HTTP) and 443 (HTTPS)
- Restrict database access to application server only

6. **Regular Backups**
```bash
# Daily backup script
*/0 * * * * pg_dump anypos > /backups/anypos_$(date +\%Y\%m\%d_\%H\%M\%S).sql
```

---

## Performance Tuning

### Database Optimization
```sql
-- Add indexes (auto-created, but verify)
CREATE INDEX idx_user_username ON users(username);
CREATE INDEX idx_product_code ON products(code);
CREATE INDEX idx_sale_date ON sales(created_at);
```

### Application Optimization
```python
# In config.py
DATABASE_ECHO = False  # Disable query logging in production
SQLALCHEMY_POOL_SIZE = 20
SQLALCHEMY_POOL_PRE_PING = True
```

### Gunicorn Optimization
```bash
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --max-requests 1000 \
  --timeout 60 \
  --bind 0.0.0.0:8000
```

---

## Monitoring & Logging

### Application Logs
```bash
# View logs
tail -f /var/log/anypos/app.log
```

### Database Logs
```bash
# PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql.log
```

### Health Check
```bash
curl http://localhost:8000/health
```

---

## Getting Help

1. Check [README.md](README.md)
2. Review [DEVELOPMENT.md](DEVELOPMENT.md)
3. Check [FEATURES.md](FEATURES.md)
4. Visit API docs: http://localhost:8000/docs
5. GitHub Issues (if applicable)

---

## Support

For detailed setup support, refer to the documentation or create an issue in the project repository.

**Installation Completed! 🎉**

Your AnyPos POS system is now ready to use. Login with:
- Username: admin
- Password: admin123
