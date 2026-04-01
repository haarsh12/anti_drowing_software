# Quick Fix Guide - Anti-Drowning System

## 🚨 Common Issues and Solutions

### Issue 1: "ModuleNotFoundError: No module named 'jwt'"

**Solution:**
```bash
cd backend_anti
pip install python-jose[cryptography]==3.3.0
python main.py
```

Or run the fix script:
```bash
cd backend_anti
fix_jwt.bat
```

### Issue 2: Backend won't start

**Check these steps:**
1. Make sure you're in the correct directory:
   ```bash
   cd backend_anti
   ```

2. Activate virtual environment (if using one):
   ```bash
   venv\Scripts\activate
   ```

3. Install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the server:
   ```bash
   python main.py
   ```

### Issue 3: Frontend won't start

**Solution:**
```bash
cd frontend_anti
npm install
npm run dev
```

### Issue 4: Mobile app can't connect

**Solution:**
1. Find your computer's IP address:
   ```bash
   ipconfig
   ```

2. Update the IP in `application_mobile/anti_drowing_app/lib/services/api_service.dart`:
   ```dart
   static const List<String> baseUrls = [
     'http://10.0.2.2:8000',           // Android emulator
     'http://YOUR_IP_HERE:8000',       // Replace with your IP
     'http://192.168.1.100:8000',      // Example IP
   ];
   ```

3. Restart the mobile app:
   ```bash
   cd application_mobile/anti_drowing_app
   flutter run
   ```

## 🚀 Quick Start Commands

### Start Everything at Once:
```bash
start_system.bat
```

### Start Backend Only:
```bash
cd backend_anti
python main.py
```

### Start Frontend Only:
```bash
cd frontend_anti
npm run dev
```

### Test the System:
```bash
python test_complete_system.py
```

## 📱 Mobile App Setup

1. **Install Flutter dependencies:**
   ```bash
   cd application_mobile/anti_drowing_app
   flutter pub get
   ```

2. **Update API endpoints with your IP:**
   - Edit `lib/services/api_service.dart`
   - Replace `YOUR_COMPUTER_IP` with actual IP from `ipconfig`

3. **Run the app:**
   ```bash
   flutter run
   ```

## 🔌 ESP32 Setup

1. **Install Arduino IDE and libraries:**
   - ArduinoJson
   - LoRa by Sandeep Mistry

2. **Update configuration in `esp32_code.ino`:**
   ```cpp
   const char* ssid = "YOUR_WIFI_NAME";
   const char* password = "YOUR_WIFI_PASSWORD";
   const char* serverURL = "http://YOUR_COMPUTER_IP:8000/api/alert";
   ```

3. **Upload to ESP32 and monitor Serial output**

## 🧪 Testing

### Test Backend API:
```bash
curl http://localhost:8000/api/alerts
```

### Test Emergency Alert:
```bash
curl -X POST http://localhost:8000/api/alert \
  -H "Content-Type: application/json" \
  -d '{"device_id":"test","danger":true,"latitude":20.9517,"longitude":75.1681}'
```

### Run Complete System Test:
```bash
python test_complete_system.py
```

## 📞 Still Having Issues?

1. **Check if ports are available:**
   - Backend: http://localhost:8000
   - Frontend: http://localhost:5173

2. **Check firewall settings** - Allow Python and Node.js through firewall

3. **Restart all services** and try again

4. **Check the console output** for specific error messages

## 🎯 System URLs

- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **Web Dashboard:** http://localhost:5173
- **Mobile App:** Connect to your computer's IP address

## ✅ Success Indicators

- Backend: "Uvicorn running on http://0.0.0.0:8000"
- Frontend: "Local: http://localhost:5173"
- Mobile App: Shows login screen and can connect
- ESP32: Serial monitor shows "System ready - Listening for LoRa data..."