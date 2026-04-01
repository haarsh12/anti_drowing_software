# ESP32 Communication Debugging Guide

## 🚨 Enhanced ESP32 Debugging System

Your backend now has **comprehensive ESP32 debugging** that shows detailed information about every communication from your ESP32 devices.

## ✅ What's Enhanced

### 1. **Backend Terminal Logging**
Every ESP32 communication now shows:
```
================================================================================
📡 ESP32 COMMUNICATION RECEIVED
================================================================================
🕐 Timestamp: 2026-04-01 21:35:08
📱 Device ID: ESP32_POOL_MAIN
🚨 Danger Status: 🔴 EMERGENCY!
📍 Latitude: 20.9517
📍 Longitude: 75.1681
📍 Location: Jalgaon Main Swimming Pool
📶 RSSI: -67 dBm
📶 WiFi RSSI: -45 dBm
💓 Heartbeat: False
🧪 Test Mode: False
⏱️  Device Uptime: 123.5 seconds
📻 NRF Status: active
================================================================================
💾 Alert saved to database with ID: 8
🚨 EMERGENCY ALERT CREATED - Mobile notifications will be triggered!
================================================================================
```

### 2. **Request Middleware Logging**
Shows all incoming HTTP requests:
```
📥 INCOMING REQUEST: POST /api/alert
🌐 Client IP: 192.168.1.100
🕐 Time: 21:35:08
🤖 ESP32 Device Detected!
📱 User-Agent: ESP32HTTPClient/1.0
📤 RESPONSE: 201 (0.045s)
✅ Success Response: 201
--------------------------------------------------
```

### 3. **Enhanced ESP32 Code**
The ESP32 receiver now sends comprehensive data:
- System information (heap, chip ID, SDK version)
- Network details (WiFi SSID, IP address, signal strength)
- NRF24L01 status and communication quality
- Device uptime and timestamps
- Current operational state

## 🧪 Testing Your ESP32 Debugging

### Step 1: Start Backend with Debug Mode
```bash
cd backend_anti
python main.py
```

**Expected Output:**
```
🚀 Starting Anti-Drowning Emergency System API...
📊 Dashboard: http://localhost:8000/docs
🔗 API Base: http://localhost:8000/api
🚨 ESP32 Debug Mode: ENABLED
📡 All ESP32 communications will be logged in detail
============================================================
```

### Step 2: Test with Simulation Script
```bash
python test_esp32_communication.py
```

This simulates various ESP32 scenarios:
- Emergency alerts
- Safe status updates
- Heartbeat messages
- Test communications
- NRF24L01 data

### Step 3: Connect Real ESP32
1. **Upload enhanced receiver code** to your ESP32
2. **Configure WiFi and server URL** in the code
3. **Power on ESP32** and watch backend terminal
4. **Trigger emergency** on sender ESP32

## 📊 What You'll See in Backend Terminal

### 🚨 Emergency Alert Example:
```
================================================================================
📡 ESP32 COMMUNICATION RECEIVED
================================================================================
🕐 Timestamp: 2026-04-01 21:35:08
📱 Device ID: ESP32_NRF_RECEIVER_01
🚨 Danger Status: 🔴 EMERGENCY!
📍 Latitude: 20.9517
📍 Longitude: 75.1681
📍 Location: Jalgaon Main Swimming Pool
📶 WiFi RSSI: -45 dBm
⏱️  Device Uptime: 125.3 seconds
📻 NRF Status: active
💾 Free Heap: 245760 bytes
🆔 Chip ID: 240ac4123456
📱 SDK Version: v4.4.2
================================================================================
🆕 Creating new device: ESP32_NRF_RECEIVER_01
✅ Device created successfully
💾 Alert saved to database with ID: 15
🚨 EMERGENCY ALERT CREATED - Mobile notifications will be triggered!
================================================================================
```

### 💓 Heartbeat Example:
```
================================================================================
📡 ESP32 COMMUNICATION RECEIVED
================================================================================
🕐 Timestamp: 2026-04-01 21:36:15
📱 Device ID: ESP32_NRF_RECEIVER_01
🚨 Danger Status: 🟢 SAFE
📍 Latitude: 20.9517
📍 Longitude: 75.1681
📍 Location: Jalgaon Main Swimming Pool
📶 WiFi RSSI: -42 dBm
💓 Heartbeat: True
⏱️  Device Uptime: 185.7 seconds
📻 NRF Status: active
🌐 WiFi SSID: YourWiFiNetwork
🌐 Local IP: 192.168.1.150
💾 Free Heap: 243840 bytes
⚡ CPU Frequency: 240 MHz
================================================================================
📱 Using existing device: ESP32_NRF_RECEIVER_01
💾 Alert saved to database with ID: 16
✅ Safe status recorded
================================================================================
```

## 🔧 Debugging Common Issues

### Issue 1: ESP32 Not Connecting
**Backend shows:** No ESP32 communications

**Check:**
1. **WiFi credentials** in ESP32 code
2. **Server URL** matches your computer's IP
3. **Network connectivity** - same WiFi network
4. **Firewall settings** - allow port 8000

**ESP32 Serial Monitor should show:**
```
✅ WiFi connected successfully!
IP address: 192.168.1.150
✅ Server connection test successful! Response code: 201
```

### Issue 2: NRF24L01 Not Working
**Backend shows:** `📻 NRF Status: failed`

**Check:**
1. **Power supply** - exactly 3.3V for NRF24L01
2. **Wire connections** - verify all pins
3. **Capacitors** - add 10µF + 100nF near NRF VCC
4. **Distance** - keep sender/receiver close for testing

**ESP32 Serial Monitor should show:**
```
✅ NRF24L01 initialized successfully
📡 NRF24L01 data received!
Raw data: '1'
```

### Issue 3: Data Not Reaching Backend
**Backend shows:** Request received but missing fields

**Check:**
1. **JSON format** in ESP32 code
2. **Content-Type header** set to `application/json`
3. **Payload size** - ensure not too large
4. **Server response** in ESP32 serial monitor

### Issue 4: Emergency Alerts Not Triggering Mobile App
**Backend shows:** Alert created but no mobile notifications

**Check:**
1. **Mobile app** is running and logged in
2. **Notification permissions** granted
3. **Polling service** active (every 3 seconds)
4. **Backend IP** configured in mobile app

## 📱 ESP32 Serial Monitor Debugging

### Enhanced ESP32 Output:
```
📤 Sending detailed data to server...
🌐 URL: http://192.168.1.162:8000/api/alert
📊 Payload size: 387 bytes
📄 Full payload: {"device_id":"ESP32_NRF_RECEIVER_01","danger":true,...}
✅ Server response code: 201
📥 Server response: {"message":"Alert created successfully","data":{"id":15}}
🚨 EMERGENCY ALERT SENT SUCCESSFULLY!

📊 DETAILED SYSTEM STATUS:
==================================================
🌐 WiFi: ✅ Connected (-42 dBm, YourWiFiNetwork)
🖥️  Server: ✅ Reachable
📻 NRF24L01: ✅ Active
🚨 Current State: 🔴 DANGER
💾 Free Heap: 243840 bytes
⏱️  Uptime: 185 seconds
🆔 Chip ID: 240ac4123456
==================================================
```

## 🎯 Production Debugging Tips

### 1. **Monitor Backend Logs**
- Keep backend terminal open during testing
- Look for ESP32 communication patterns
- Check for missing or incorrect data

### 2. **Use ESP32 Serial Monitor**
- Monitor ESP32 output for connection issues
- Check payload data before sending
- Verify server responses

### 3. **Test Communication Flow**
```
ESP32 Sender → NRF24L01 → ESP32 Receiver → Backend → Mobile App
```

### 4. **Debug Each Stage**
- **Stage 1:** Sender ESP32 serial output
- **Stage 2:** Receiver ESP32 NRF data reception
- **Stage 3:** Backend terminal ESP32 logs
- **Stage 4:** Mobile app notification logs

## 🚀 Advanced Debugging Features

### 1. **Payload Analysis**
Backend shows complete JSON payload from ESP32:
```json
{
  "device_id": "ESP32_NRF_RECEIVER_01",
  "danger": true,
  "latitude": 20.9517,
  "longitude": 75.1681,
  "location_name": "Jalgaon Main Swimming Pool",
  "wifi_rssi": -45,
  "uptime": 125300,
  "nrf_status": "active",
  "free_heap": 245760,
  "chip_id": "240ac4123456"
}
```

### 2. **Performance Monitoring**
- Request processing time
- Memory usage tracking
- Network signal strength
- Device uptime monitoring

### 3. **Error Tracking**
- Failed communications logged
- Network connectivity issues
- Database errors with details
- Recovery attempts tracked

## 📞 Troubleshooting Checklist

### ✅ **ESP32 Hardware:**
- [ ] Power supply stable (3.3V for NRF24L01)
- [ ] All connections secure
- [ ] LEDs indicating status
- [ ] Serial monitor showing activity

### ✅ **Network:**
- [ ] ESP32 connected to WiFi
- [ ] Same network as backend server
- [ ] Firewall allows port 8000
- [ ] IP address correct in ESP32 code

### ✅ **Backend:**
- [ ] Server running on port 8000
- [ ] Debug logs appearing in terminal
- [ ] Database connections working
- [ ] API endpoints responding

### ✅ **Mobile App:**
- [ ] App running and logged in
- [ ] Notification permissions granted
- [ ] Polling service active
- [ ] Backend IP configured correctly

Your ESP32 debugging system is now **fully enhanced** and ready to help you troubleshoot any communication issues!