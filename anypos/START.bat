@echo off
REM START.bat - Start AnyPos POS System (All-in-One)
REM Just double-click this file to start the entire application

echo.
echo ========================================
echo   AnyPos POS System - Starting...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [1/5] Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [2/5] Activating Python environment...
call venv\Scripts\activate.bat

REM Install Python dependencies
echo [3/5] Installing Python dependencies...
pip install -q -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo [4/5] Creating configuration file (.env)...
    copy .env.example .env >nul
)

REM Initialize database
echo [5/5] Initializing database...
cd backend
python ..\scripts\init_data.py >nul 2>&1
cd ..

REM Start backend in a new window
echo.
echo ========================================
echo   Starting Backend Server...
echo ========================================
start "AnyPos Backend" cmd /k venv\Scripts\activate.bat && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start frontend in a new window
echo.
echo ========================================
echo   Starting Frontend Server...
echo ========================================
cd frontend
start "AnyPos Frontend" cmd /k "%COMSPEC% /c set PATH=C:\Program Files\nodejs;%PATH% && npm run dev"
cd ..

REM Display ready message
echo.
echo ========================================
echo   SUCCESS! AnyPos is Running
echo ========================================
echo.
echo Open your browser and go to:
echo   http://localhost:5173
echo.
echo Login with:
echo   Username: admin
echo   Password: admin123
echo.
echo API Documentation (if needed):
echo   http://localhost:8000/docs
echo.
echo Press any key to close this window...
pause
