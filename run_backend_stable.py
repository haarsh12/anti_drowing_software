#!/usr/bin/env python3
"""
Stable Backend Server for ESP32 Debugging
Runs without auto-reload to prevent interruption of debug logs
"""

import uvicorn
import sys
import os

# Add the backend_anti directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend_anti'))

def main():
    print("🚀 Starting Anti-Drowning Emergency System API (STABLE MODE)")
    print("📊 Dashboard: http://localhost:8000/docs")
    print("🔗 API Base: http://localhost:8000/api")
    print("🚨 ESP32 Debug Mode: ENABLED")
    print("📡 All ESP32 communications will be logged in detail")
    print("🔒 Auto-reload DISABLED for stable debugging")
    print("=" * 60)
    
    # Run server without auto-reload for stable ESP32 debugging
    uvicorn.run(
        "backend_anti.main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable auto-reload for stable debugging
        log_level="info"
    )

if __name__ == "__main__":
    main()