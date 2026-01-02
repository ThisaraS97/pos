#!/bin/bash
# startup.sh - Start AnyPos development environment

echo "🚀 Starting AnyPos Development Environment..."

# Check Python
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "   Please update .env with your configuration"
fi

# Initialize database
echo "🗄️  Initializing database..."
cd backend
python ../scripts/init_data.py

# Start backend
echo "🎯 Starting FastAPI server..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000
