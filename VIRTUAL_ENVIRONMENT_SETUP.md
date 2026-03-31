# 🐍 Virtual Environment Setup - Complete Guide

## ✅ Setup Complete!

Your IoT Alert Dashboard backend now has a properly configured virtual environment with all dependencies installed.

## 📁 What Was Created

```
backend_anti/
├── venv/                    # Virtual environment (isolated Python)
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Development dependencies
├── .gitignore              # Git ignore rules
├── setup_venv.py           # Automated setup script
├── activate_venv.bat       # Windows activation script
├── activate_venv.sh        # Linux/Mac activation script
├── run_server.bat          # Windows server launcher
├── run_server.sh           # Linux/Mac server launcher
└── BACKEND_SETUP.md        # Detailed setup guide
```

## 🚀 Quick Start Commands

### Windows Users:
```bash
# Option 1: Double-click the batch file
run_server.bat

# Option 2: Command line
venv\Scripts\python.exe main.py
```

### Linux/Mac Users:
```bash
# Option 1: Run the shell script
./run_server.sh

# Option 2: Command line
venv/bin/python main.py
```

## 📦 Installed Packages

Your virtual environment includes:

### Core Framework
- ✅ **FastAPI 0.104.1** - Modern web framework
- ✅ **Uvicorn 0.24.0** - ASGI server with WebSocket support
- ✅ **Pydantic 2.5.0** - Data validation

### Database
- ✅ **SQLAlchemy 2.0.23** - ORM for database operations
- ✅ **psycopg2-binary 2.9.9** - PostgreSQL adapter

### Configuration
- ✅ **python-dotenv 1.0.0** - Environment variable management
- ✅ **python-multipart 0.0.6** - File upload support

### HTTP Client
- ✅ **requests 2.31.0** - HTTP library for testing
- ✅ **httpx 0.25.2** - Async HTTP client

### Development Tools
- ✅ **pytest 7.4.3** - Testing framework
- ✅ **pytest-asyncio 0.21.1** - Async testing support
- ✅ **black 23.11.0** - Code formatter
- ✅ **flake8 6.1.0** - Code linter
- ✅ **isort 5.12.0** - Import sorter

## 🧪 Testing Your Setup

### 1. Database Connection Test
```bash
# Windows
venv\Scripts\python.exe test_db_connection.py

# Linux/Mac
venv/bin/python test_db_connection.py
```

Expected output:
```
🚀 Supabase Database Connection Test
==================================================
✅ Database connected successfully!
✅ Tables created successfully!
✅ All database tests passed successfully!
```

### 2. API Integration Test
```bash
# Windows
venv\Scripts\python.exe verify_supabase.py

# Linux/Mac
venv/bin/python verify_supabase.py
```

Expected output:
```
🧪 Testing IoT Alert System API with Supabase
============================================================
✅ Health check: healthy
✅ Danger alert created: ID 3
✅ Safe alert created: ID 4
🎉 Supabase integration test completed!
```

### 3. Start the Server
```bash
# Windows
run_server.bat

# Linux/Mac
./run_server.sh
```

Expected output:
```
🚀 Starting IoT Alert Dashboard Backend Server
===============================================
✅ Virtual environment found
🔄 Starting FastAPI server...

📍 Server will be available at: http://localhost:8000
📖 API Documentation: http://localhost:8000/docs
🔍 Health Check: http://localhost:8000/health
```

## 🔧 Virtual Environment Benefits

### Isolation
- ✅ **Separate Python environment** - No conflicts with system Python
- ✅ **Isolated dependencies** - Project-specific package versions
- ✅ **Clean development** - Easy to recreate and share

### Version Control
- ✅ **requirements.txt** - Exact dependency versions
- ✅ **Reproducible builds** - Same environment on any machine
- ✅ **Easy deployment** - Consistent production environment

### Development Workflow
- ✅ **Easy activation** - Simple scripts to start working
- ✅ **Testing isolation** - Run tests without affecting system
- ✅ **Multiple projects** - Different environments for different projects

## 🛠 Manual Commands (If Needed)

### Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### Install Additional Packages
```bash
# After activation
pip install package_name

# Update requirements.txt
pip freeze > requirements.txt
```

### Deactivate Virtual Environment
```bash
deactivate
```

## 🔍 Troubleshooting

### Virtual Environment Not Found
```bash
# Recreate virtual environment
python -m venv venv

# Install dependencies
venv\Scripts\pip.exe install -r requirements.txt  # Windows
venv/bin/pip install -r requirements.txt          # Linux/Mac
```

### Permission Errors (Linux/Mac)
```bash
# Make scripts executable
chmod +x activate_venv.sh
chmod +x run_server.sh
```

### Package Installation Errors
```bash
# Upgrade pip first
venv\Scripts\python.exe -m pip install --upgrade pip  # Windows
venv/bin/python -m pip install --upgrade pip          # Linux/Mac

# Then install requirements
venv\Scripts\pip.exe install -r requirements.txt      # Windows
venv/bin/pip install -r requirements.txt              # Linux/Mac
```

### Port Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Kill the process or change port in .env file
```

## 🎯 Next Steps

1. ✅ **Virtual environment is ready**
2. ✅ **All dependencies installed**
3. ✅ **Database connection tested**
4. ✅ **API endpoints verified**

### Ready to Run:
```bash
# Start backend server
run_server.bat        # Windows
./run_server.sh       # Linux/Mac

# Start frontend (in another terminal)
cd ../frontend_anti
npm install
npm run dev
```

### Your IoT Alert Dashboard is now fully operational! 🎉

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Database**: Connected to Supabase

The virtual environment ensures your project runs consistently across different machines and doesn't interfere with other Python projects on your system.