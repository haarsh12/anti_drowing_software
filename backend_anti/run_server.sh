#!/bin/bash
echo "🚀 Starting IoT Alert Dashboard Backend Server"
echo "==============================================="

# Check if virtual environment exists
if [ ! -f "venv/bin/python" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    echo "Then run: venv/bin/pip install -r requirements.txt"
    exit 1
fi

echo "✅ Virtual environment found"
echo "🔄 Starting FastAPI server..."
echo ""
echo "📍 Server will be available at: http://localhost:8000"
echo "📖 API Documentation: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "==============================================="

# Start the server using virtual environment Python
venv/bin/python main.py