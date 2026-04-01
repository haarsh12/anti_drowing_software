@echo off
echo 🔧 Fixing Flutter app compilation issues...
echo.

echo 📦 Cleaning Flutter build cache...
flutter clean

echo 📥 Getting dependencies...
flutter pub get

echo 🚀 Running the app...
flutter run

pause