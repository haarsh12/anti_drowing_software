# IoT Alert Dashboard - Complete Setup Guide

This guide will help you set up the complete LoRa-based emergency alert system with backend, frontend, and ESP32 components.

## System Overview

```
LoRa Sender → ESP32 Receiver → Backend API → Frontend Dashboard
```

## Prerequisites

- Python 3.8+ (for backend)
- Node.js 16+ (for frontend)
- Arduino IDE (for ESP32)
- PostgreSQL database (local or Supabase)

## 1. Backend Setup (FastAPI)

### Step 1: Install Python Dependencies

```bash
cd backend_anti
pip install -r requirements.txt
```

### Step 2: Database Setup

#### Option A: Supabase (Recommended)
1. Go to [supabase.com](https://supabase.com) and create account
2. Create new project
3. Go to Settings → Database
4. Copy the connection string

#### Option B: Local PostgreSQL
1. Install PostgreSQL
2. Create database: `iot_alerts`
3. Note your credentials

### Step 3: Configure Environment

Edit `.env` file in `backend_anti/`:

```env
# For Supabase
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

# For local PostgreSQL
# DATABASE_URL=postgresql://username:password@localhost:5432/iot_alerts

HOST=0.0.0.0
PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### Step 4: Run Backend Server

```bash
cd backend_anti
python main.py
```

The API will be available at: `http://localhost:8000`

**Test the API:**
- Visit `http://localhost:8000/docs` for interactive documentation
- Health check: `http://localhost:8000/health`

## 2. Frontend Setup (React)

### Step 1: Install Dependencies

```bash
cd frontend_anti
npm install
```

### Step 2: Start Development Server

```bash
npm run dev
```

The dashboard will be available at: `http://localhost:3000`

### Step 3: Verify Connection

- Open the dashboard in your browser
- Check that it shows "Waiting for device data..."
- Connection status should show "Connected" if backend is running

## 3. ESP32 Setup

### Step 1: Install Arduino IDE Libraries

Open Arduino IDE and install these libraries:
- **ArduinoJson** by Benoit Blanchon
- **LoRa** by Sandeep Mistry

### Step 2: Hardware Connections

Connect LoRa module (SX1276/SX1278) to ESP32:

```
LoRa Module    ESP32 Pin
VCC         →  3.3V
GND         →  GND
SCK         →  GPIO 18
MISO        →  GPIO 19
MOSI        →  GPIO 23
CS          →  GPIO 5
RST         →  GPIO 14
DIO0        →  GPIO 2
```

Optional LEDs:
```
LED Type       ESP32 Pin
WiFi LED    →  GPIO 12
Danger LED  →  GPIO 13
Safe LED    →  GPIO 15
```

### Step 3: Configure ESP32 Code

Edit `esp32_code.ino`:

```cpp
// WiFi Configuration
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Backend Server Configuration
const char* serverURL = "http://192.168.1.100:8000/api/alert";  // Your computer's IP
const String deviceID = "esp32_1";
```

**Find your computer's IP:**
- Windows: `ipconfig`
- Mac/Linux: `ifconfig`

### Step 4: Upload Code

1. Connect ESP32 to computer
2. Select board: "ESP32 Dev Module"
3. Select correct COM port
4. Upload the code
5. Open Serial Monitor (115200 baud)

## 4. Testing the System

### Test 1: Backend API

```bash
# Test creating an alert
curl -X POST http://localhost:8000/api/alert \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test_device",
    "danger": true,
    "latitude": 18.52,
    "longitude": 73.85
  }'

# Get all alerts
curl http://localhost:8000/api/alerts
```

### Test 2: ESP32 Connection

1. Check Serial Monitor output
2. Verify WiFi connection
3. Verify LoRa initialization
4. Look for heartbeat messages every 30 seconds

### Test 3: LoRa Communication

Send data from another LoRa device in format:
- Danger: `"1,18.5204,73.8567"`
- Safe: `"0,18.5204,73.8567"`

### Test 4: End-to-End Flow

1. Send LoRa data to ESP32
2. Check ESP32 Serial Monitor for received data
3. Verify data appears in backend logs
4. Check frontend dashboard for new alert
5. Verify map marker and table update

## 5. Production Deployment

### Backend Deployment

1. **Using Docker:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

2. **Using Cloud Services:**
- Deploy to Heroku, Railway, or DigitalOcean
- Update CORS_ORIGINS in .env
- Use production database

### Frontend Deployment

1. **Build for production:**
```bash
npm run build
```

2. **Deploy to:**
- Vercel: `vercel --prod`
- Netlify: Upload `dist` folder
- GitHub Pages: Use GitHub Actions

3. **Update API endpoint:**
Edit `src/services/api.js` with production backend URL

## 6. Troubleshooting

### Common Issues

**Backend Issues:**
- Database connection failed → Check DATABASE_URL
- CORS errors → Update CORS_ORIGINS in .env
- Port already in use → Change PORT in .env

**Frontend Issues:**
- API connection failed → Check backend URL in api.js
- Map not loading → Check internet connection
- Build errors → Run `npm install` again

**ESP32 Issues:**
- WiFi connection failed → Check credentials and signal
- LoRa initialization failed → Check wiring
- HTTP errors → Verify server URL and network

### Debug Commands

**Check backend logs:**
```bash
cd backend_anti
python main.py
```

**Check database:**
```sql
-- Connect to your database and run:
SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 10;
```

**Test ESP32 without LoRa:**
Add this to `loop()` function for testing:
```cpp
// Uncomment for testing
// simulateLoRaData();
// delay(10000);
```

## 7. System Monitoring

### Health Checks

- Backend: `GET /health`
- Frontend: Check connection indicator
- ESP32: Monitor Serial output

### Logs

- Backend: Console output
- Frontend: Browser console (F12)
- ESP32: Serial Monitor

### Performance

- Database: Monitor query performance
- API: Check response times
- ESP32: Monitor memory usage

## 8. Security Considerations

### Production Security

1. **Backend:**
   - Use HTTPS
   - Add authentication
   - Validate input data
   - Use environment variables

2. **Database:**
   - Use strong passwords
   - Enable SSL connections
   - Regular backups

3. **ESP32:**
   - Secure WiFi credentials
   - Use encrypted communication
   - Regular firmware updates

## 9. Scaling

### High Availability

- Use load balancers
- Database clustering
- Multiple ESP32 devices
- Redundant servers

### Performance

- Database indexing
- API caching
- CDN for frontend
- WebSocket for real-time updates

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review component README files
3. Check Serial Monitor output
4. Verify network connectivity
5. Test each component individually

The system is designed to be beginner-friendly while maintaining production-ready architecture. Each component can be developed and tested independently.