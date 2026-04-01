@echo off
echo Installing missing JWT dependency...
pip install python-jose[cryptography]==3.3.0
echo.
echo JWT dependency installed successfully!
echo.
echo Starting backend server...
python main.py