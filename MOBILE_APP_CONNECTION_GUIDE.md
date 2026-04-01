# Mobile App Connection Fix Guide

## IMMEDIATE SOLUTION

Your IP address is: **192.168.1.162**

### Step 1: Start Backend with Network Access

**STOP** your current backend and restart it properly:

```bash
cd backend_anti
run_server.bat
```

The script now starts with `--host 0.0.0.0` so your mobile app can connect.

### Step 2: Test Connection

1. **Test from your phone's browser**: 
   - Open: `http://192.168.1.162:8000`
   - Should show FastAPI welcome page

2. **Test API endpoint**:
   - Open: `http://192.168.1.162:8000/api/alerts`
   - Should show JSON response

### Step 3: Test Mobile App

Your mobile app is already configured with the correct IP (`192.168.1.162`). Once you restart the backend properly, it should connect.

### Step 4: Test Map Markers

Run this script to add test alerts with exact Jalgaon coordinates:

```bash
python test_jalgaon_alerts.py
```

This will create:
- 🔴 **Red markers**: Current/danger alerts
- ⚪ **Grey markers**: Previous/safe alerts

## Exact Jalgaon Coordinates

The map now uses these precise coordinates:
- **Center**: 20.947409, 75.554987 (Jalgaon Railway Station)
- **Test locations**: Multiple points around Jalgaon city

## What You Should See

1. **Web Dashboard** (`http://localhost:3000`):
   - Map centered on Jalgaon, Maharashtra
   - Red and grey markers at different locations
   - Real-time updates

2. **Mobile App**:
   - "Online" status in top-right
   - List of emergency cases
   - Auto-refresh every 5 seconds

## Troubleshooting

If mobile app still shows "Offline":
1. Make sure backend is running with `run_server.bat` (not `python main.py`)
2. Check Windows Firewall isn't blocking port 8000
3. Ensure phone and computer are on same WiFi network