@echo off
REM startup.bat - Start AnyPos development environment (Windows)

echo 🚀 Starting AnyPos Development Environment...

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -q -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo ⚙️  Creating .env file...
    copy .env.example .env
    echo    Please update .env with your configuration
)

REM Initialize database
echo 🗄️  Initializing database...
cd backend
python ../scripts/init_data.py

REM Start backend
echo 🎯 Starting FastAPI server...
uvicorn main:app --reload --host 0.0.0.0 --port 8000
