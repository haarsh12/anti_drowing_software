#!/usr/bin/env python3
"""
Test ESP32 Backend Connection
Simulates ESP32 sending data to backend to verify the connection works
"""

import requests
import json
import time
from datetime import datetime

# Backend configuration
BACKEND_URL = "http://192.168.1.162:8000/api/alert"

def test_esp32_data():
    """Test sending ESP32-like data to backend"""
    
    print("🧪 TESTING ESP32 BACKEND CONNECTION")
    print("=" * 50)
    print(f"Backend URL: {BACKEND_URL}")
    print()
    
    # Test data matching ESP32 format
    test_data = {
        "device_id": "ESP32_ESPNOW_RECEIVER_01",
        "danger": True,
        "latitude": 20.947489,
        "longitude": 75.554932,
        "location_name": "Emergency Alert System",
        "sender_id": 1,
        "data_source": "esp_now",
        "wifi_rssi": -63,
        "uptime": 123456,
        "timestamp": int(time.time() * 1000),
        "heartbeat": False,
        "test": True,
        "free_heap": 200000,
        "chip_id": "88:13:BF:63:A5:E0"
    }
    
    try:
        print("📤 Sending test data to backend...")
        print(f"📊 Data: {json.dumps(test_data, indent=2)}")
        print()
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "ESP32HTTPClient/1.0"
        }
        
        response = requests.post(BACKEND_URL, json=test_data, headers=headers, timeout=10)
        
        print(f"📡 HTTP Response Code: {response.status_code}")
        print(f"📥 Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ SUCCESS! Backend received and processed the data correctly!")
            print("🎯 Your ESP32 should be able to send data to the backend now.")
        else:
            print(f"❌ FAILED! Expected status code 201, got {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR!")
        print("🔧 Possible issues:")
        print("   • Backend server is not running")
        print("   • Wrong IP address")
        print("   • Firewall blocking connection")
        print("   • Network connectivity issues")
        print()
        print("💡 Solutions:")
        print("   1. Start backend: python backend_anti/main.py")
        print("   2. Check IP address with: python get_ip_address.py")
        print("   3. Test manually: http://192.168.1.162:8000/docs")
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")

def test_backend_health():
    """Test if backend is running"""
    try:
        health_url = "http://192.168.1.162:8000/health"
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            print("✅ Backend health check passed!")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except:
        print("❌ Backend is not reachable!")
        return False

def main():
    print("🚀 ESP32 BACKEND CONNECTION TEST")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test backend health first
    print("1️⃣ Testing backend health...")
    if test_backend_health():
        print()
        print("2️⃣ Testing ESP32 data submission...")
        test_esp32_data()
    else:
        print()
        print("❌ Backend is not running or not reachable!")
        print("🔧 Please start the backend server first:")
        print("   python backend_anti/main.py")
    
    print()
    print("=" * 50)
    print("🔍 Next steps:")
    print("1. If test passed: Upload updated ESP32 code")
    print("2. If test failed: Check backend server and network")
    print("3. Monitor ESP32 serial output for HTTP responses")
    print("4. Check dashboard for new alerts")

if __name__ == "__main__":
    main()