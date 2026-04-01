@echo off
echo 🔄 Restarting Backend for ESP32 Debug Mode
echo ==========================================

echo 🛑 Stopping any existing backend processes...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

echo 🚀 Starting backend in debug mode...
cd backend_anti
python main.py

pause