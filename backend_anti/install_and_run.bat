@echo off
echo ========================================
echo Backend Setup and Installation
echo ========================================
echo.

echo Installing Python dependencies...
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install sqlalchemy==2.0.23
pip install pydantic==2.5.0
pip install python-multipart==0.0.6
pip install passlib[bcrypt]==1.7.4
pip install python-jose[cryptography]==3.3.0
pip install python-dotenv==1.0.0
pip install requests==2.31.0

echo.
echo ========================================
echo Dependencies installed successfully!
echo ========================================
echo.

echo Starting backend server...
python main.py

pause