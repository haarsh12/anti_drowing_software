"""
Main FastAPI application for IoT Alert Dashboard
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from database import create_tables
from routes.alerts import router as alerts_router

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="IoT Alert Dashboard API",
    description="Backend API for LoRa-based emergency alert system",
    version="1.0.0"
)

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(alerts_router)

@app.on_event("startup")
async def startup_event():
    """
    Create database tables on startup
    """
    create_tables()
    print("Database tables created successfully")

@app.get("/")
async def root():
    """
    Root endpoint for health check
    """
    return {
        "message": "IoT Alert Dashboard API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug
    )