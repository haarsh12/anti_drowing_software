# 🚀 IoT Alert Dashboard - Backend Setup Guide

## 📋 Prerequisites

- **Python 3.8+** (Check with `python --version`)
- **Git** (for version control)
- **Supabase account** (or local PostgreSQL)

## 🛠 Quick Setup (Automated)

### Option 1: Automated Setup Script

```bash
cd backend_anti
python setup_venv.py
```

This script will:
- ✅ Check Python version compatibility
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Verify installation

### Option 2: Manual Setup

```bash
cd backend_anti

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🔧 Environment Configuration

### 1. Database Setup (Already Done ✅)

Your Supabase database is already configured:
```env
DATABASE_URL=postgresql://postgres.ugsaergbbnjaqdnqcgjz:harsha12er45@aws-1-ap-south-1.pooler.supabase.com:5432/postgres
```

### 2. Environment Variables

The `.env` file is already configured with:
- ✅ Supabase connection string
- ✅ Server configuration
- ✅ CORS settings

## 🚀 Running the Backend

### Method 1: Using Activation Scripts

**Windows:**
```bash
# Double-click or run:
activate_venv.bat
# Then run:
python main.py
```

**Linux/Mac:**
```bash
./activate_venv.sh
# Then run:
python main.py
```

### Method 2: Manual Activation

```bash
# Activate environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Start server
python main.py
```

## 🧪 Testing the Backend

### 1. Database Connection Test
```bash
python test_db_connection.py
```

Expected output:
```
🚀 Supabase Database Connection Test
==================================================
✅ Database connected successfully!
✅ Tables created successfully!
✅ All database tests passed successfully!
```

### 2. API Endpoints Test
```bash
python verify_supabase.py
```

Expected output:
```
🧪 Testing IoT Alert System API with Supabase
============================================================
✅ Health check: healthy
✅ Danger alert created: ID 3
✅ Safe alert created: ID 4
✅ Retrieved 3 alerts from Supabase
🎉 Supabase integration test completed!
```

### 3. Manual API Testing

**Health Check:**
```bash
curl http://localhost:8000/health
# or
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

**Create Alert:**
```bash
curl -X POST http://localhost:8000/api/alert \
  -H "Content-Type: application/json" \
  -d '{"device_id": "test", "danger": true, "latitude": 18.52, "longitude": 73.85}'
```

**Get Alerts:**
```bash
curl http://localhost:8000/api/alerts
```

## 📁 Project Structure

```
backend_anti/
├── main.py                 # FastAPI application entry point
├── database.py             # Database configuration
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas
├── routes/
│   └── alerts.py           # API routes
├── requirements.txt        # Production dependencies
├── requirements-dev.txt    # Development dependencies
├── .env                    # Environment variables
├── .gitignore             # Git ignore rules
├── setup_venv.py          # Automated setup script
├── activate_venv.bat      # Windows activation script
├── activate_venv.sh       # Linux/Mac activation script
├── test_db_connection.py  # Database test script
├── verify_supabase.py     # API test script
└── BACKEND_SETUP.md       # This file
```

## 🔍 API Documentation

Once the server is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/alert` | Create new alert (ESP32) |
| GET | `/api/alerts` | Get all alerts |
| GET | `/api/alerts/latest` | Get latest alert |
| GET | `/api/alerts/{device_id}` | Get alerts by device |

## 🐛 Troubleshooting

### Common Issues

**1. Python version error:**
```
❌ Python 3.8 or higher is required
```
**Solution:** Install Python 3.8+ from python.org

**2. Virtual environment activation fails:**
```
❌ Virtual environment not found!
```
**Solution:** Run `python setup_venv.py` first

**3. Database connection error:**
```
❌ Database connection failed
```
**Solution:** Check your internet connection and Supabase credentials

**4. Port already in use:**
```
❌ Address already in use
```
**Solution:** Kill the process using port 8000 or change the port in `.env`

**5. Module not found:**
```
❌ ModuleNotFoundError: No module named 'fastapi'
```
**Solution:** Activate virtual environment first

### Debug Commands

**Check virtual environment:**
```bash
# Should show venv path
which python
# or
where python
```

**List installed packages:**
```bash
pip list
```

**Check server logs:**
```bash
python main.py
# Look for any error messages
```

**Test database manually:**
```bash
python -c "from database import engine; print(engine.url)"
```

## 🔧 Development Setup

### Install Development Dependencies
```bash
pip install -r requirements-dev.txt
```

### Code Formatting
```bash
# Format code
black .

# Sort imports
isort .

# Lint code
flake8 .
```

### Running Tests
```bash
pytest
```

## 🚀 Production Deployment

### Environment Variables for Production
```env
DEBUG=False
HOST=0.0.0.0
PORT=8000
DATABASE_URL=your_production_database_url
CORS_ORIGINS=https://your-frontend-domain.com
```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

### Cloud Deployment Options
- **Heroku**: `git push heroku main`
- **Railway**: Connect GitHub repository
- **DigitalOcean App Platform**: Deploy from GitHub
- **AWS EC2**: Use systemd service

## 📊 Monitoring

### Health Checks
- **Endpoint**: GET `/health`
- **Expected Response**: `{"status": "healthy"}`

### Logs
- Server logs appear in console
- Database operations logged automatically
- Error tracking with proper HTTP status codes

### Performance
- FastAPI automatic request/response validation
- SQLAlchemy connection pooling
- Async support for high concurrency

## 🎯 Next Steps

1. ✅ **Backend is running** on http://localhost:8000
2. 🎨 **Start frontend**: `cd ../frontend_anti && npm run dev`
3. 📱 **Configure ESP32**: Update WiFi credentials and server IP
4. 🧪 **Test end-to-end**: Send LoRa data and see it in dashboard

## 📞 Support

If you encounter issues:
1. Check this troubleshooting guide
2. Verify all prerequisites are installed
3. Run the test scripts to isolate the problem
4. Check server logs for detailed error messages

Your IoT Alert Dashboard backend is now ready for production use! 🎉