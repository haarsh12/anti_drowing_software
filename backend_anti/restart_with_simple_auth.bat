@echo off
echo ========================================
echo Restarting Backend with Simple Auth
echo ========================================
echo.

echo Cleaning old database...
if exist anti_drowning.db del anti_drowning.db

echo Starting backend with simple authentication...
python main.py

pause