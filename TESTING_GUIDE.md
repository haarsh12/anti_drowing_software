# 🚨 Emergency System Testing Guide

## 📋 Overview

This guide helps you test your complete emergency response system:
**ESP32 Simulation → Backend → Web Dashboard → Mobile App**

## 🛠 Test Files Created

### 1. `test_emergency_system.py` - Complete Test Suite
- **Full system testing** with multiple test scenarios
- **Interactive menu** for different test types
- **Comprehensive reporting** of results
- **Stress testing** capabilities

### 2. `quick_test.py` - Single Alert Test
- **Quick test** - sends one emergency alert
- **Simple and fast** for basic verification
- **Perfect for initial testing**

### 3. `run_emergency_test.bat` - Windows Runner
- **One-click testing** on Windows
- **Automatic setup** and dependency checking
- **User-friendly** batch file

## 🚀 How to Run Tests

### Option 1: Quick Test (Recommended for first time)
```bash
python quick_test.py
```

### Option 2: Full Test Suite
```bash
python test_emergency_system.py
```

### Option 3: Windows Batch File
```bash
run_emergency_test.bat
```

## 📱 Test Scenarios

### 1. Single Emergency Alert
- Sends one emergency signal
- Tests basic system functionality
- Verifies backend → web → mobile flow

### 2. Multiple Alerts Test
- Sends 3 different emergency alerts
- Tests system handling of multiple signals
- Verifies data consistency

### 3. Location-Based Test
- Tests alerts from different NYC locations:
  - Central Park
  - Brooklyn Bridge  
  - Times Square
  - Statue of Liberty

### 4. Stress Test
- Sends 5-10 rapid alerts
- Tests system performance under load
- Verifies no data loss

## ✅ What to Check After Running Tests

### 1. Backend (http://127.0.0.1:8000/api/alerts)
- Should show new alerts in JSON format
- Verify alert data is correct
- Check timestamps are recent

### 2. Web Dashboard (http://localhost:3000)
- Should display new alerts on the map
- Alert cards should show correct information
- Auto-refresh should work (every 5 seconds)

### 3. Mobile App
- Should show "Online" status
- New alerts should appear in the list
- Case cards should display correctly
- Auto-refresh should work

## 🔧 Prerequisites

### 1. Backend Running
```bash
cd backend_anti
python -m uvicorn main:app --reload
```

### 2. Web Dashboard Running (Optional)
```bash
cd frontend_anti
npm start
```

### 3. Mobile App Running (Optional)
```bash
cd application_mobile/anti_drowing_app
flutter run
```

### 4. Python Dependencies
```bash
pip install requests
```

## 📊 Sample Test Output

```
🚨 EMERGENCY SYSTEM FULL TEST SUITE 🚨
============================================================

🚨 Testing Backend Connection
============================================================
✅ Backend is running and accessible

🚨 Single Emergency Alert Test
============================================================
✅ Emergency alert sent successfully! Alert ID: 123
ℹ️ Device: ESP32_TEST_1704123456, Danger: True, Location: (40.7128, -74.0060)
✅ Check your web dashboard - you should see the new alert!
✅ Check your mobile app - it should refresh and show the alert!
ℹ️ Total alerts in system: 1

🚨 Multiple Emergency Alerts Test (3 alerts)
============================================================
ℹ️ Sending alert 1/3...
✅ Emergency alert sent successfully! Alert ID: 124
ℹ️ Sending alert 2/3...
✅ Emergency alert sent successfully! Alert ID: 125
ℹ️ Sending alert 3/3...
✅ Emergency alert sent successfully! Alert ID: 126
✅ Successfully sent 3/3 alerts
ℹ️ Total alerts in system: 4

🚨 Test Results Summary
============================================================
✅ Single Alert Test: PASSED
✅ Multiple Alerts Test: PASSED
✅ Location Test: PASSED
✅ Stress Test: PASSED
ℹ️ Overall: 4/4 tests passed
```

## 🐛 Troubleshooting

### Backend Connection Issues
```
❌ Cannot connect to backend: Connection refused
```
**Solution**: Start your backend server first

### Mobile App Not Updating
- Check if app is connected (should show "Online")
- Try pull-to-refresh on the home screen
- Restart the app if needed

### Web Dashboard Not Updating
- Check browser console for errors
- Refresh the page manually
- Verify backend URL in dashboard code

## 📈 Advanced Testing

### Custom Alert Data
Modify `test_emergency_system.py` to send custom data:
```python
alert_data = {
    "device_id": "YOUR_DEVICE_ID",
    "danger": True,  # or False
    "latitude": 40.7128,  # Your coordinates
    "longitude": -74.0060
}
```

### Automated Testing
Set up automated tests to run every few minutes:
```bash
# Run test every 5 minutes
while true; do
    python quick_test.py
    sleep 300
done
```

## 🎯 Success Criteria

Your system is working correctly if:

✅ **Backend**: Receives and stores alerts  
✅ **Web Dashboard**: Displays alerts on map and in table  
✅ **Mobile App**: Shows alerts as cases with correct status  
✅ **Real-time Updates**: All components refresh automatically  
✅ **Data Consistency**: Same data across all platforms  

## 🚀 Next Steps

1. **Run Quick Test**: Start with `python quick_test.py`
2. **Verify All Components**: Check backend, web, and mobile
3. **Run Full Suite**: Use `python test_emergency_system.py`
4. **Add Firebase**: Set up push notifications for mobile
5. **Deploy**: Move to production environment

---

**Happy Testing! Your emergency response system is ready for action!** 🚨📱🌐