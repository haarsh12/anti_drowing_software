#!/usr/bin/env python3
"""
Simple Backend Debug - Shows ESP32 communications clearly
Run this instead of the main backend to see ESP32 debug logs
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend_anti'))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
from datetime import datetime

app = FastAPI(title="ESP32 Debug Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.url.path == "/api/alert" and request.method == "POST":
        # Get the request body
        body = await request.body()
        
        print("\n" + "="*80)
        print("📡 ESP32 COMMUNICATION RECEIVED")
        print("="*80)
        print(f"🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🌐 Client IP: {request.client.host}")
        print(f"📱 User-Agent: {request.headers.get('user-agent', 'Unknown')}")
        
        try:
            data = json.loads(body.decode())
            print(f"📱 Device ID: {data.get('device_id', 'Unknown')}")
            print(f"🚨 Danger: {'🔴 EMERGENCY!' if data.get('danger') else '🟢 SAFE'}")
            print(f"📍 Location: {data.get('location_name', 'Unknown')}")
            print(f"📍 Coordinates: {data.get('latitude', 0)}, {data.get('longitude', 0)}")
            
            if 'wifi_rssi' in data:
                print(f"📶 WiFi RSSI: {data['wifi_rssi']} dBm")
            if 'uptime' in data:
                print(f"⏱️  Uptime: {data['uptime']/1000:.1f} seconds")
            if 'free_heap' in data:
                print(f"💾 Free Heap: {data['free_heap']} bytes")
            if 'chip_id' in data:
                print(f"🆔 Chip ID: {data['chip_id']}")
            if 'test' in data:
                print(f"🧪 Test Mode: {data['test']}")
                
            print(f"📄 Full JSON: {json.dumps(data, indent=2)}")
            
        except Exception as e:
            print(f"❌ Error parsing JSON: {e}")
            print(f"📄 Raw body: {body.decode()}")
        
        print("="*80)
    
    response = await call_next(request)
    return response

@app.post("/api/alert")
async def create_alert(request: Request):
    """Simple alert endpoint that just returns success"""
    body = await request.body()
    
    try:
        data = json.loads(body.decode())
        alert_id = 999  # Fake ID for testing
        
        print(f"✅ Alert processed successfully!")
        print(f"🆔 Assigned Alert ID: {alert_id}")
        
        if data.get('danger'):
            print("🚨 EMERGENCY ALERT - Mobile notifications would be triggered!")
        else:
            print("✅ Safe status recorded")
        
        print("="*80 + "\n")
        
        return {
            "message": "Alert created successfully",
            "data": {
                "id": alert_id,
                "alert_id": alert_id,
                "device_id": data.get("device_id"),
                "danger": data.get("danger"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "timestamp": datetime.now().isoformat()
            }
        }
    except Exception as e:
        print(f"❌ Error processing alert: {e}")
        return {"error": "Failed to process alert"}

@app.get("/health")
async def health():
    return {"status": "healthy", "message": "ESP32 Debug Backend Running"}

if __name__ == "__main__":
    print("🚀 ESP32 DEBUG BACKEND STARTING")
    print("="*50)
    print("📡 This backend will show detailed ESP32 logs")
    print("🔗 URL: http://localhost:8000/api/alert")
    print("🔍 Watch for ESP32 communications below...")
    print("="*50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="error")