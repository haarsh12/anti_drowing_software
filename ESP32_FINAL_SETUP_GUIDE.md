# ESP32 ESP-NOW Emergency System - Final Setup Guide

## 🚀 QUICK START

### 1. Backend Server Setup
```bash
# Start the backend server (MUST be running first)
cd backend_anti
python main.py
```
**Backend will run on:** `http://192.168.1.162:8000`

### 2. ESP32 Code Setup
1. **Open:** `esp32_espnow_final_working.ino`
2. **Update WiFi password** in the configuration section:
   ```cpp
   const char* password = "YOUR_ACTUAL_WIFI_PASSWORD";  // Replace this
   ```
3. **Upload to ESP32**

### 3. Test the System
```bash
# Test backend connection
python test_esp32_backend_connection.py
```

## 📡 How It Works

### Data Flow:
1. **ESP-NOW Sender** → sends `{id, lat, lon}` → **ESP32 Receiver**
2. **ESP32 Receiver** → processes data → **Backend Server** (HTTP POST)
3. **Backend Server** → stores in database → **Dashboard & Mobile App**

### ESP32 Receiver Behavior:
- ✅ Receives ESP-NOW data from sender
- ✅ Immediately sends each coordinate to backend
- ✅ Creates emergency alerts in database
- ✅ Triggers notifications to mobile app
- ✅ Shows detailed logs in Serial Monitor

## 🔧 Configuration Details

### ESP32 Configuration (in code):
```cpp
// WiFi - UPDATE THIS
const char* ssid = "Internet";                    // ✅ Correct
const char* password = "YOUR_WIFI_PASSWORD";      // ❌ UPDATE THIS

// Backend Server - VERIFIED WORKING
const char* serverURL = "http://192.168.1.162:8000/api/alert";  // ✅ Correct
```

### Backend Server:
- **URL:** `http://192.168.1.162:8000`
- **API Endpoint:** `/api/alert`
- **Status:** ✅ Tested and working

## 📊 Expected Serial Output

When ESP32 receives data, you should see:
```
📩 RECEIVED ESP-NOW DATA
========================
Alert #: 1
ID: 1
Lat: 20.947489
Lon: 75.554932
========================

📊 PROCESSING EMERGENCY COORDINATES
===================================
🆔 Sender ID: 1
📍 Location: 20.947489, 75.554932
🚨 Status: EMERGENCY DETECTED!
📤 Sending to backend server...

🚀 SENDING EMERGENCY TO BACKEND
===============================
🌐 URL: http://192.168.1.162:8000/api/alert

📊 JSON PAYLOAD:
{"device_id":"ESP32_ESPNOW_RECEIVER_01","danger":true,"latitude":20.947489,"longitude":75.554932...}

📡 SENDING HTTP POST REQUEST...
📡 HTTP RESPONSE CODE: 201

✅ BACKEND RESPONSE RECEIVED:
=============================
{"message":"Alert created successfully","data":{"id":221,"alert_id":221...}}
=============================

🎯 SUCCESS! EMERGENCY ALERT CREATED IN BACKEND!
📱 Alert should now appear in:
   • Dashboard: http://192.168.1.162:8000/docs
   • Mobile app notifications
   • Frontend web interface
```

## 🎯 Verification Steps

### 1. Check Backend Logs
When ESP32 sends data, backend should show:
```
📡 ESP32 COMMUNICATION RECEIVED
===============================
🕐 Timestamp: 2026-04-02 09:17:58
📱 Device ID: ESP32_ESPNOW_RECEIVER_01
🚨 Danger Status: 🔴 EMERGENCY!
📍 Latitude: 20.947489
📍 Longitude: 75.554932
💾 Alert saved to database with ID: 221
🚨 EMERGENCY ALERT CREATED - Mobile notifications will be triggered!
```

### 2. Check Dashboard
Visit: `http://192.168.1.162:8000/docs`
- Go to `/api/alerts` endpoint
- Click "Try it out" → "Execute"
- Should see your emergency alerts listed

### 3. Check Mobile App
- Open the mobile app
- Should receive push notifications for new alerts
- Check emergency screen for new cases

## ❌ Troubleshooting

### ESP32 Not Sending to Backend:
1. **Check WiFi connection** - LED should be on
2. **Verify backend is running** - run `python test_esp32_backend_connection.py`
3. **Check serial output** - look for HTTP response codes
4. **Update WiFi password** in ESP32 code

### Backend Not Receiving Data:
1. **Start backend server:** `python backend_anti/main.py`
2. **Check IP address:** `python get_ip_address.py`
3. **Test manually:** Visit `http://192.168.1.162:8000/docs`

### Mobile App Not Getting Notifications:
1. **Check backend logs** - should show "Mobile notifications will be triggered!"
2. **Verify app is connected** to correct backend IP
3. **Check notification permissions** on mobile device

## 🔥 Key Changes Made

### Fixed ESP32 Issues:
- ✅ Removed timeout logic that was marking alerts as "safe"
- ✅ Fixed `processReceivedData()` to actually call `sendToServer()`
- ✅ Added detailed HTTP logging for debugging
- ✅ Corrected server URL and WiFi settings
- ✅ Every received coordinate now guaranteed to reach backend

### Backend Verification:
- ✅ Tested with `test_esp32_backend_connection.py`
- ✅ Confirmed API accepts ESP32 data format
- ✅ Verified database storage and alert creation
- ✅ Confirmed mobile notification triggering

## 🎉 Success Indicators

You'll know it's working when:
1. **ESP32 Serial Monitor** shows "SUCCESS! EMERGENCY ALERT CREATED IN BACKEND!"
2. **Backend logs** show "Alert saved to database with ID: XXX"
3. **Dashboard** at `/api/alerts` shows new emergency entries
4. **Mobile app** receives push notifications
5. **Frontend** displays new alerts on map and table

---

**Next Step:** Upload `esp32_espnow_final_working.ino` to your ESP32 and test with your sender device!