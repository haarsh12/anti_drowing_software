# IoT Alert Dashboard - Backend

FastAPI backend for the LoRa-based emergency alert system.

## Setup Instructions

### 1. Install Dependencies

```bash
cd backend_anti
pip install -r requirements.txt
```

### 2. Database Setup

#### Option A: Local PostgreSQL
1. Install PostgreSQL
2. Create database: `iot_alerts`
3. Update `.env` with your database credentials

#### Option B: Supabase (Recommended)
1. Create account at [supabase.com](https://supabase.com)
2. Create new project
3. Go to Settings > Database
4. Copy connection string and update `.env`

### 3. Environment Configuration

Update `.env` file with your settings:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/iot_alerts
# OR for Supabase:
# DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
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