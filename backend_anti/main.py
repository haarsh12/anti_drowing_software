"""
FastAPI main application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import alerts
from routes import simple_auth as auth
from database import init_database
import uvicorn
import time
from datetime import datetime

# Initialize database
init_database()

# Create FastAPI app
app = FastAPI(
    title="Anti-Drowning Emergency System API",
    description="Real-time emergency response system for drowning prevention",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware to log all requests (especially from ESP32)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log incoming request details
    if request.url.path.startswith("/api/"):
        print(f"\n📥 INCOMING REQUEST: {request.method} {request.url.path}")
        print(f"🌐 Client IP: {request.client.host}")
        print(f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}")
        
        # Log headers for debugging
        user_agent = request.headers.get("user-agent", "Unknown")
        if "ESP32" in user_agent or "Arduino" in user_agent:
            print(f"🤖 ESP32 Device Detected!")
        print(f"📱 User-Agent: {user_agent}")
    
    response = await call_next(request)
    
    # Log response details
    if request.url.path.startswith("/api/"):
        process_time = time.time() - start_time
        print(f"📤 RESPONSE: {response.status_code} ({process_time:.3f}s)")
        if response.status_code >= 400:
            print(f"❌ Error Response: {response.status_code}")
        else:
            print(f"✅ Success Response: {response.status_code}")
        print("-" * 50)
    
    return response

# Include routers
app.include_router(auth.router)
app.include_router(alerts.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Anti-Drowning Emergency System API",
        "version": "2.0.0",
        "status": "active",
        "endpoints": {
            "auth": "/api/auth",
            "alerts": "/api/alerts",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "System operational"}

if __name__ == "__main__":
    print("🚀 Starting Anti-Drowning Emergency System API...")
    print("📊 Dashboard: http://localhost:8000/docs")
    print("🔗 API Base: http://localhost:8000/api")
    print("🚨 ESP32 Debug Mode: ENABLED")
    print("📡 All ESP32 communications will be logged in detail")
    print("🔒 Auto-reload DISABLED for stable ESP32 debugging")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable auto-reload for stable ESP32 debugging
        log_level="info"
    )