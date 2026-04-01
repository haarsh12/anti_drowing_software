@echo off
echo ========================================
echo 🚨 Emergency System Test Runner
echo ========================================
echo.
echo This will test your complete system:
echo ESP32 Simulation → Backend → Web → Mobile
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if backend is running
echo 🔍 Checking if backend is running...
curl -s http://127.0.0.1:8000/ >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Backend doesn't seem to be running
    echo Please start your backend first:
    echo    cd backend_anti
    echo    python -m uvicorn main:app --reload
    echo.
    echo Press any key to continue anyway...
    pause >nul
)

REM Install required packages if needed
echo 📦 Installing required packages...
pip install requests >nul 2>&1

REM Run the test
echo.
echo 🚀 Starting Emergency System Test...
echo.
python test_emergency_system.py

echo.
echo ✅ Test completed!
pause