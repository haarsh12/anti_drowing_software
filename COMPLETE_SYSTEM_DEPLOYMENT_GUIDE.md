# Complete Anti-Drowning Emergency System - Deployment Guide

## 🚀 System Overview

This is a complete, production-ready anti-drowning emergency system with:
- **Real-time emergency detection** via ESP32 + LoRa
- **Mobile app** for guards with system-level notifications
- **Web dashboard** for monitoring and management
- **Backend API** with database integration
- **Authentication system** with JWT tokens

## 📋 Prerequisites

### Software Requirements
- **Node.js** (v16 or higher)
- **Python** (3.8 or higher)
- **Flutter** (3.0 or higher)
- **Git**

### Hardware Requirements (ESP32)
- ESP32 development board
- LoRa module (SX1276/SX1278)
- LEDs for status indication (optional)
- WiFi network access

## 🔧 Step 1: Backend Setup

### 1.1 Navigate to Backend Directory
```bash
cd backend_anti
```

### 1.2 Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 1.3 Install Dependencies
```bash
pip install -r requirements.txt
```

### 1.4 Configure Database
The system uses SQLite by default. For production, configure PostgreSQL in `database.py`.

### 1.5 Start Backend Server
```bash
python main.py
```

The backend will be available at `http://localhost:8000`

**Important**: Note your computer's IP address for mobile app and ESP32 configuration:
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

## 🌐 Step 2: Frontend Web Dashboard Setup

### 2.1 Navigate to Frontend Directory
```bash
cd frontend_anti
```

### 2.2 Install Dependencies
```bash
npm install
```

### 2.3 Start Development Server
```bash
npm run dev
```

The web dashboard will be available at `http://localhost:5173`

## 📱 Step 3: Mobile App Setup

### 3.1 Navigate to Mobile App Directory
```bash
cd application_mobile/anti_drowing_app
```

### 3.2 Install Flutter Dependencies
```bash
flutter pub get
```

### 3.3 Configure API Endpoints
Edit `lib/services/api_service.dart` and update the IP addresses in the `baseUrls` array:

```dart
static const List<String> baseUrls = [
  'http://10.0.2.2:8000',           // Android emulator
  'http://YOUR_COMPUTER_IP:8000',   // Replace with your actual IP
  'http://192.168.0.100:8000',      // Alternative IP range
  'http://127.0.0.1:8000',          // Localhost
];
```

### 3.4 Build and Run Mobile App

#### For Android Emulator:
```bash
flutter run
```

#### For Physical Android Device:
1. Enable Developer Options and USB Debugging
2. Connect device via USB
3. Run: `flutter run`

#### For iOS (Mac only):
```bash
flutter run -d ios
```

## 🔌 Step 4: ESP32 Configuration

### 4.1 Hardware Setup
Connect your LoRa module to ESP32:
- **VCC** → 3.3V
- **GND** → GND
- **SCK** → GPIO 18
- **MISO** → GPIO 19
- **MOSI** → GPIO 23
- **CS** → GPIO 5
- **RST** → GPIO 14
- **DIO0** → GPIO 2

### 4.2 Software Setup
1. Install Arduino IDE
2. Install ESP32 board support
3. Install required libraries:
   - ArduinoJson
   - LoRa by Sandeep Mistry

### 4.3 Configure ESP32 Code
Edit `esp32_code.ino` and update:

```cpp
// WiFi Configuration
const char* ssid = "YOUR_WIFI_NETWORK_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

// Backend Server Configuration
const char* serverURL = "http://YOUR_COMPUTER_IP:8000/api/alert";
```

### 4.4 Upload Code
1. Connect ESP32 to computer
2. Select correct board and port in Arduino IDE
3. Upload the code
4. Monitor Serial output for connection status

## 🔐 Step 5: Authentication Setup

### 5.1 Create Admin Account
Use the mobile app or make a direct API call:

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin User",
    "phone": "+1234567890",
    "password": "secure_password",
    "role": "admin"
  }'
```

### 5.2 Create Guard Accounts
Guards can register through the mobile app or via API.

## 🧪 Step 6: System Testing

### 6.1 Test Backend API
```bash
# Test alert creation
curl -X POST http://localhost:8000/api/alert \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test_device",
    "danger": true,
    "latitude": 20.9517,
    "longitude": 75.1681
  }'
```

### 6.2 Test Mobile App
1. Register a new guard account
2. Login with credentials
3. Verify cases list loads
4. Test map functionality
5. Verify notifications work

### 6.3 Test ESP32 Integration
1. Monitor Serial output for WiFi connection
2. Verify server connectivity
3. Send test LoRa data: `1,20.9517,75.1681`
4. Check if alert appears in mobile app and web dashboard

## 🚨 Step 7: Emergency System Testing

### 7.1 Create Test Emergency
Send LoRa data to ESP32 in format: `1,latitude,longitude`

Example: `1,20.9517,75.1681`

### 7.2 Verify System Response
1. **ESP32**: LEDs should indicate danger status
2. **Backend**: Alert should be stored in database
3. **Web Dashboard**: Alert should appear in real-time
4. **Mobile App**: 
   - System notification should appear
   - Full-screen emergency overlay should show
   - Guards can respond with actions

## 📊 Step 8: Production Deployment

### 8.1 Backend Production Setup
1. Configure PostgreSQL database
2. Set up proper environment variables
3. Use production WSGI server (Gunicorn)
4. Configure reverse proxy (Nginx)
5. Set up SSL certificates

### 8.2 Frontend Production Build
```bash
cd frontend_anti
npm run build
```

Deploy the `dist` folder to your web server.

### 8.3 Mobile App Production Build
```bash
cd application_mobile/anti_drowing_app

# Android
flutter build apk --release

# iOS (Mac only)
flutter build ios --release
```

## 🔧 Configuration Files Summary

### Backend Configuration
- `backend_anti/main.py` - Main server file
- `backend_anti/database.py` - Database configuration
- `backend_anti/models.py` - Database models

### Frontend Configuration
- `frontend_anti/src/services/api.js` - API endpoints
- `frontend_anti/package.json` - Dependencies

### Mobile App Configuration
- `application_mobile/anti_drowing_app/lib/services/api_service.dart` - API configuration
- `application_mobile/anti_drowing_app/pubspec.yaml` - Dependencies

### ESP32 Configuration
- `esp32_code.ino` - Main ESP32 code with WiFi and server settings

## 🚨 Emergency System Features

### Mobile App Features
- ✅ **Real authentication** with JWT tokens
- ✅ **System-level notifications** (works when app is closed)
- ✅ **Full-screen emergency overlay** (non-dismissible)
- ✅ **Real-time data** from backend API
- ✅ **Guard response tracking** with backend integration
- ✅ **Google Maps integration** for location viewing
- ✅ **Scrollable interface** with proper error handling
- ✅ **Logout functionality** with user menu

### Web Dashboard Features
- ✅ **Real-time alert monitoring**
- ✅ **Interactive map** with alert locations
- ✅ **Guard response tracking**
- ✅ **Auto-refresh** every 5 seconds
- ✅ **Responsive design** for all screen sizes

### Backend Features
- ✅ **RESTful API** with proper error handling
- ✅ **JWT authentication** with role-based access
- ✅ **Real database integration** (SQLite/PostgreSQL)
- ✅ **Guard response tracking**
- ✅ **Device management**
- ✅ **System logging**

### ESP32 Features
- ✅ **LoRa communication** for emergency detection
- ✅ **WiFi connectivity** with auto-reconnect
- ✅ **HTTP POST** to backend API
- ✅ **LED status indicators**
- ✅ **Heartbeat monitoring**
- ✅ **Error recovery** and retry logic

## 📞 Support and Troubleshooting

### Common Issues

#### Mobile App Won't Connect
1. Check if backend server is running
2. Verify IP address in `api_service.dart`
3. Ensure phone and computer are on same network
4. Check firewall settings

#### ESP32 Won't Connect
1. Verify WiFi credentials
2. Check server URL and IP address
3. Monitor Serial output for error messages
4. Verify LoRa module connections

#### Notifications Not Working
1. Grant notification permissions in phone settings
2. Ensure app is not in battery optimization
3. Check if backend is sending alerts
4. Verify polling is active

### Getting Help
1. Check Serial monitor output for ESP32 issues
2. Check browser console for web dashboard issues
3. Check mobile app logs for connection issues
4. Verify all services are running on correct ports

## 🎯 System Architecture

```
[LoRa Sensor] → [ESP32] → [WiFi] → [Backend API] → [Database]
                                        ↓
[Web Dashboard] ← [Real-time Updates] ← [Mobile App]
```

The system is now fully functional with real data integration, proper authentication, and production-ready features!