@echo off
echo ========================================
echo Running Single Emergency Case Test
echo ========================================
echo.

echo Make sure your backend is running first!
echo Backend should be at: http://localhost:8000
echo.

pause

echo Running comprehensive test...
python test_single_emergency_case.py

echo.
echo Test completed!
pause