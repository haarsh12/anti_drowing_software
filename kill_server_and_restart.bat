@echo off
echo Killing any existing servers on port 8000...

REM Kill any Python processes using port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    echo Killing process %%a
    taskkill /f /pid %%a 2>nul
)

REM Wait a moment
timeout /t 2 /nobreak >nul

echo Starting fresh backend server...
cd /d "%~dp0backend_anti"

REM Activate virtual environment and start server
call venv\Scripts\activate.bat
python main.py

pause