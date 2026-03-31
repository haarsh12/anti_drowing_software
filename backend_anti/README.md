# IoT Alert Dashboard - Backend

FastAPI backend for the LoRa-based emergency alert system.

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend_anti
pip install -r requirements.txt
```

### 2. Database Setup - Supabase (Configured)

✅ **Already configured with Supabase!**

Your database connection details:
- Host: `aws-1-ap-south-1.pooler.supabase.com`
- Database: `postgres`
- User: `postgres.ugsaergbbnjaqdnqcgjz`
- Connection string is already set in `.env`

### 3. Environment Configuration

✅ **Already configured!** The `.env` file contains:
```env
DATABASE_URL=postgresql://postgres.ugsaergbbnjaqdnqcgjz:harsha12er45@aws-1-ap-south-1.pooler.supabase.com:5432/postgres
```

### 4. Run the Server

```bash
python main.py
```

The API will be available at: `http://localhost:8000`

## API Endpoints

- `POST /api/alert` - Create new alert (ESP32 endpoint)
- `GET /api/alerts` - Get all alerts
- `GET /api/alerts/latest` - Get latest alert
- `GET /api/alerts/{device_id}` - Get alerts by device ID
- `GET /` - Health check
- `GET /docs` - Interactive API documentation

## Project Structure

```
backend_anti/
├── main.py           # FastAPI application entry point
├── database.py       # Database configuration
├── models.py         # SQLAlchemy models
├── schemas.py        # Pydantic schemas
├── routes/
│   └── alerts.py     # Alert API routes
├── requirements.txt  # Python dependencies
├── .env             # Environment variables
└── README.md        # This file
```