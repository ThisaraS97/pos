# START.ps1 - Start AnyPos POS System (Single Command)
# Run this file to start the entire application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AnyPos POS System - Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Set execution policy for this session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned -Force | Out-Null

# Check Python
try {
    python --version | Out-Null
} catch {
    Write-Host "ERROR: Python is not installed" -ForegroundColor Red
    Write-Host "Please install from https://www.python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Node.js
try {
    node --version | Out-Null
} catch {
    Write-Host "ERROR: Node.js is not installed" -ForegroundColor Red
    Write-Host "Please install from https://nodejs.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "[1/5] Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "[2/5] Activating Python environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Install Python dependencies
Write-Host "[3/5] Installing Python dependencies..." -ForegroundColor Yellow
pip install -q -r requirements.txt 2>&1 | Out-Null

# Create .env if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "[4/5] Creating configuration file (.env)" -ForegroundColor Yellow
    Copy-Item .env.example .env
}

# Initialize database
Write-Host "[5/5] Initializing database..." -ForegroundColor Yellow
cd .\backend
python ..\scripts\init_data.py 2>&1 | Out-Null
cd ..

# Start backend
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Backend Server..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$pwd\backend'; & '..\venv\Scripts\Activate.ps1'; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

# Wait for backend to start
Start-Sleep -Seconds 3

# Start frontend
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Starting Frontend Server..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
$frontendCmd = {
    cd frontend
    `$env:Path = "C:\Program Files\nodejs;`$env:Path"
    & 'C:\Program Files\nodejs\npm.cmd' run dev
}
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd

# Show success message
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  SUCCESS! AnyPos is Running" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Open your browser and go to:" -ForegroundColor Green
Write-Host "  http://localhost:5173" -ForegroundColor Cyan
Write-Host ""
Write-Host "Login with:" -ForegroundColor Green
Write-Host "  Username: admin" -ForegroundColor Cyan
Write-Host "  Password: admin123" -ForegroundColor Cyan
Write-Host ""
Write-Host "API Documentation:" -ForegroundColor Green
Write-Host "  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
