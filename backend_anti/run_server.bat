@echo off
echo 🚀 Starting IoT Alert Dashboard Backend Server
echo ===============================================

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then run: venv\Scripts\pip.exe install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ Virtual environment found
echo 🔄 Starting FastAPI server...
echo.
echo 📍 Server will be available at: http://localhost:8000
echo 📖 API Documentation: http://localhost:8000/docs
echo 🔍 Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo ===============================================

REM Start the server using virtual environment Python
venv\Scripts\python.exe main.py