@echo off
echo 🔄 Restart Backend and Clear Database
echo =====================================
echo.

echo 1️⃣ The backend needs to be restarted to load the new delete endpoint
echo    Please follow these steps:
echo.
echo    📋 Manual Steps:
echo    1. Stop your current backend server (Ctrl+C)
echo    2. Restart it with: python backend_anti/main.py
echo    3. Wait for "Server started" message
echo    4. Press any key here to continue...
echo.

pause

echo.
echo 2️⃣ Now clearing database and creating single test case...
python clear_and_create_one.py

echo.
echo 3️⃣ Done! Check your mobile app and website now.
echo.

pause