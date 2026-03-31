@echo off
REM Activation script for Windows
echo 🚀 Activating IoT Alert Dashboard Backend Environment
echo =====================================================

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run: python setup_venv.py
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Show status
echo ✅ Virtual environment activated!
echo 📁 Current directory: %CD%
echo 🐍 Python version:
python --version
echo 📦 Pip version:
pip --version

echo.
echo 📋 Available commands:
echo   python main.py              - Start the FastAPI server
echo   python verify_supabase.py   - Test database connection
echo   python test_db_connection.py - Test database setup
echo   pip list                    - Show installed packages
echo   deactivate                  - Exit virtual environment
echo.

REM Keep the command prompt open
cmd /k