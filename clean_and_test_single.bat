@echo off
echo 🧹 Clean Database and Test Single Case
echo ========================================
echo.

echo 1️⃣ Clearing all previous cases...
python clear_all_cases.py
echo.

echo 2️⃣ Waiting for cleanup to complete...
timeout /t 3 /nobreak > nul
echo.

echo 3️⃣ Creating single test case...
python test_single_case.py
echo.

echo 4️⃣ Test completed!
echo.
echo 💡 Next steps:
echo    📱 Check mobile app for emergency notification
echo    🌐 Open website: http://localhost:3000
echo    🔍 Verify only 1 case appears
echo    👁️ Test "View Details" button
echo    🗺️ Test "View Maps" button
echo.

pause