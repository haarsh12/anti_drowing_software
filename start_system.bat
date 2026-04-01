@echo off
echo ========================================
echo Anti-Drowning Emergency System Startup
echo ========================================
echo.

echo Installing backend dependencies (if needed)...
cd backend_anti
pip install python-jose[cryptography]==3.3.0 >nul 2>&1

echo Starting Backend Server...
start "Backend Server" cmd /k "python main.py"
cd ..

echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

echo Starting Frontend Dashboard...
cd frontend_anti
start "Frontend Dashboard" cmd /k "npm run dev"
cd ..

echo.
echo ========================================
echo System Started Successfully!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Web Dashboard: http://localhost:5173
echo.
echo To test the system, run:
echo python test_complete_system.py
echo.
echo To configure mobile app:
echo 1. Find your IP address: ipconfig
echo 2. Update lib/services/api_service.dart
echo 3. Run: flutter run
echo.
echo To configure ESP32:
echo 1. Update WiFi credentials in esp32_code.ino
echo 2. Update server URL with your IP
echo 3. Upload to ESP32
echo.
pause