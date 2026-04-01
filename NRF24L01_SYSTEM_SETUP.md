# NRF24L01 Emergency Alert System Setup Guide

## 🚨 Complete NRF24L01 Communication System

This guide covers the setup of a complete NRF24L01-based emergency alert system with sender and receiver ESP32 modules.

## 📋 System Overview

### Components:
1. **Sender ESP32** - Detects emergencies and transmits alerts
2. **Receiver ESP32** - Receives alerts and forwards to backend server
3. **NRF24L01 Modules** - 2.4GHz wireless communication
4. **Backend Server** - Processes alerts and triggers mobile notifications

### Communication Flow:
```
Drowning Detection → Sender ESP32 → NRF24L01 → Receiver ESP32 → Backend → Mobile App
```

## 🔧 Hardware Requirements

### For Each ESP32 Module:
- ESP32 development board (ESP32-WROOM-32 recommended)
- NRF24L01 module (with antenna)
- Breadboard and jumper wires
- Power supply (3.3V stable)
- Capacitors: 10µF and 100nF

### Additional for Sender:
- Buzzer (5V compatible)
- LEDs: Green (status), Red (danger), Blue (transmit)
- 220Ω resistors for LEDs
- Push button (for testing)

### Additional for Receiver:
- LEDs: Green (WiFi), Red (danger), Blue (safe)
- 220Ω resistors for LEDs

## 📐 Hardware Connections

### NRF24L01 to ESP32 (Both Sender and Receiver):
```
NRF24L01    ESP32
VCC      -> 3.3V (CRITICAL: Not 5V!)
GND      -> GND
CE       -> GPIO 4
CSN      -> GPIO 5
SCK      -> GPIO 18
MOSI     -> GPIO 23
MISO     -> GPIO 19
IRQ      -> Not connected
```

### Sender ESP32 Additional Connections:
```
Component       ESP32 Pin
Buzzer (+)   -> GPIO 15
Buzzer (-)   -> GND
Status LED   -> GPIO 12 -> 220Ω -> GND
Danger LED   -> GPIO 13 -> 220Ω -> GND
Transmit LED -> GPIO 14 -> 220Ω -> GND
Test Button  -> GPIO 2 (with pull-up)
```

### Receiver ESP32 Additional Connections:
```
Component       ESP32 Pin
WiFi LED     -> GPIO 12 -> 220Ω -> GND
Danger LED   -> GPIO 13 -> 220Ω -> GND
Safe LED     -> GPIO 15 -> 220Ω -> GND
```

## ⚡ Power Supply Critical Notes

### NRF24L01 Power Requirements:
- **Voltage**: Exactly 3.3V (NOT 5V - will damage module!)
- **Current**: Up to 115mA during transmission
- **Stability**: Very sensitive to voltage drops

### Power Supply Solutions:
1. **Use ESP32's 3.3V pin** (if current is sufficient)
2. **Dedicated 3.3V regulator** (recommended for reliable operation)
3. **Add capacitors**: 10µF electrolytic + 100nF ceramic near NRF24L01 VCC

### Wiring Best Practices:
- Keep wires short (< 10cm)
- Use thick wires for power (22 AWG or thicker)
- Twist power and ground wires together
- Add capacitors as close as possible to NRF24L01

## 💻 Software Setup

### 1. Install Required Libraries

In Arduino IDE, install these libraries:
- **RF24** by TMRh20 (for NRF24L01 communication)
- **ArduinoJson** (for receiver only - JSON formatting)

### 2. Upload Sender Code

1. Open `esp32_nrf_sender_improved.ino`
2. No configuration needed for basic testing
3. Upload to sender ESP32
4. Open Serial Monitor (115200 baud)

### 3. Upload Receiver Code

1. Open `esp32_nrf_receiver.ino`
2. **CRITICAL**: Update these settings:
   ```cpp
   const char* ssid = "YOUR_WIFI_SSID";
   const char* password = "YOUR_WIFI_PASSWORD";
   const char* serverURL = "http://192.168.1.162:8000/api/alert";
   ```
3. Upload to receiver ESP32
4. Open Serial Monitor (115200 baud)

## 🧪 Testing Procedure

### Step 1: Basic NRF Communication Test

1. **Power both ESP32s** and check serial outputs
2. **Sender should show**:
   ```
   ✅ NRF24L01 initialized successfully
   🚀 System Ready - Monitoring for emergencies...
   ```
3. **Receiver should show**:
   ```
   ✅ NRF24L01 initialized successfully
   ✅ WiFi connected successfully!
   🚀 System ready - Listening for NRF data...
   ```

### Step 2: Test Emergency Alert

1. **On sender**, type `1` in Serial Monitor and press Enter
2. **Expected sender behavior**:
   - Red LED turns on
   - Buzzer starts beeping (3 sec on/off)
   - Serial shows: `🚨 EMERGENCY ALERT TRIGGERED!`
   - Transmits danger signal every 500ms

3. **Expected receiver behavior**:
   - Receives NRF data
   - Red LED turns on
   - Sends emergency alert to backend server
   - Serial shows: `🚨 EMERGENCY ALERT - Sending to server!`

### Step 3: Test Safe Status

1. **On sender**, type `0` in Serial Monitor and press Enter
2. **Expected behavior**:
   - Sender: Red LED off, buzzer stops
   - Receiver: Red LED off, blue LED on
   - Backend receives safe status

### Step 4: Test Backend Integration

1. **Start backend server**: `python backend_anti/main.py`
2. **Trigger emergency** on sender
3. **Check backend logs** for received alert
4. **Run mobile app test**: `python test_full_screen_notifications.py`
5. **Verify mobile notifications** appear

## 📊 System Status Commands

### Sender Commands (via Serial Monitor):
- `1` - Trigger emergency alert
- `0` - Clear emergency alert  
- `s` - Show system status
- `t` - Test transmission

### Status Indicators:

#### Sender LEDs:
- **Green (Status)**: System ready
- **Red (Danger)**: Emergency active
- **Blue (Transmit)**: Data transmission

#### Receiver LEDs:
- **Green (WiFi)**: WiFi connected
- **Red (Danger)**: Emergency received
- **Blue (Safe)**: Safe status

## 🔧 Troubleshooting

### NRF24L01 Not Initializing:
```
❌ NRF24L01 initialization failed!
```
**Solutions**:
1. Check power supply (must be 3.3V)
2. Verify all wire connections
3. Add capacitors near NRF24L01
4. Try different NRF24L01 module
5. Check for loose connections

### No Data Received:
```
Receiver shows no NRF data received
```
**Solutions**:
1. Verify both use same channel (108) and address ("NODE1")
2. Check antenna connections
3. Reduce distance between modules (< 10 meters for testing)
4. Check for interference (WiFi, Bluetooth)
5. Verify sender is transmitting (check serial output)

### WiFi Connection Failed:
```
❌ WiFi connection failed!
```
**Solutions**:
1. Check WiFi credentials in code
2. Verify WiFi network is available
3. Check signal strength
4. Try different WiFi network

### Server Connection Failed:
```
❌ Server connection test failed!
```
**Solutions**:
1. Verify backend server is running
2. Check IP address in serverURL
3. Test server health: `http://192.168.1.162:8000/health`
4. Check firewall settings
5. Ensure devices on same network

## 📈 Performance Optimization

### Range Improvement:
- Use NRF24L01+PA+LNA modules (with external antenna)
- Increase power level: `radio.setPALevel(RF24_PA_HIGH)`
- Use lower data rate: `radio.setDataRate(RF24_250KBPS)`
- Optimize antenna positioning

### Reliability Improvement:
- Enable auto-acknowledgment: `radio.setAutoAck(true)`
- Add retry logic in code
- Use error correction
- Monitor transmission success rate

### Power Optimization:
- Use power-down mode when idle
- Reduce transmission frequency
- Lower power level for short distances
- Use sleep modes on ESP32

## 🔄 Integration with ML Model

To integrate with your drowning detection ML model:

1. **Replace sensor input** in sender code:
   ```cpp
   void checkSensorInput() {
     // Replace this with your ML model output
     bool mlDetectedDanger = yourMLModel.predict();
     
     if (mlDetectedDanger && !dangerActive) {
       triggerEmergencyAlert();
     } else if (!mlDetectedDanger && dangerActive) {
       clearEmergencyAlert();
     }
   }
   ```

2. **Add confidence threshold**:
   ```cpp
   float confidence = yourMLModel.getConfidence();
   if (confidence > 0.85) {  // 85% confidence threshold
     triggerEmergencyAlert();
   }
   ```

## 🚀 Production Deployment

### Hardware Considerations:
- Use industrial-grade ESP32 modules
- Weatherproof enclosures for outdoor use
- Backup power supply (battery + solar)
- Professional antenna installation

### Software Considerations:
- Add watchdog timers
- Implement over-the-air updates
- Add logging and diagnostics
- Monitor system health remotely

### Network Considerations:
- Use mesh networking for large areas
- Add repeaters for extended range
- Implement redundant communication paths
- Monitor network quality

## 📞 Support and Maintenance

### Regular Checks:
- Monitor transmission success rates
- Check power supply stability
- Verify WiFi connectivity
- Test emergency procedures

### Troubleshooting Tools:
- Serial monitor for debugging
- System status commands
- LED indicators for quick diagnosis
- Backend server logs

The NRF24L01 system is now ready for testing and integration with your anti-drowning emergency system!