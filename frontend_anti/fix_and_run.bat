@echo off
echo 🔧 Fixing React frontend compilation issues...
echo.

echo 🧹 Clearing npm cache...
npm cache clean --force

echo 📦 Installing dependencies...
npm install

echo 🚀 Starting the development server...
npm start

pause