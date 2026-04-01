#!/usr/bin/env python3
"""
Test Backend Logging - Send exact ESP32 data to verify logs appear
"""

import requests
import json
import time

def test_backend_logging():
    """Send the exact same data your ESP32 is sending"""
    
    url = "http://localhost:8000/api/alert"
    
    # Exact same data your ESP32 is sending
    test_data = {
        "device_id": "ESP32_DEBUG_01",
        "danger": True,
        "latitude": 20.9517,
        "longitude": 75.1681,
        "location_name": "Jalgaon Test Pool",
        "wifi_rssi": -55,
        "uptime": 45137,
        "timestamp": 45137,
        "test": True,
        "free_heap": 228568,
        "chip_id": "e0a563bf1388"
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "ESP32HTTPClient/1.0"
    }
    
    print("🧪 TESTING BACKEND DEBUG LOGS")
    print("=" * 50)
    print("Sending exact ESP32 data to backend...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(test_data, indent=2)}")
    print()
    print("🔍 CHECK YOUR BACKEND TERMINAL FOR DEBUG LOGS!")
    print("=" * 50)
    
    try:
        response = requests.post(url, json=test_data, headers=headers, timeout=10)
        
        print(f"✅ Response Code: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Alert ID: {result['data']['id']}")
            print("✅ SUCCESS - Backend should show debug logs now!")
        else:
            print(f"❌ Unexpected response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_multiple_requests():
    """Send multiple requests to test logging"""
    
    print("\n🔥 SENDING MULTIPLE TEST REQUESTS")
    print("=" * 50)
    
    test_cases = [
        {"danger": True, "description": "Emergency Alert"},
        {"danger": False, "description": "Safe Status"},
        {"danger": True, "description": "Another Emergency"},
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📡 Test {i}: {case['description']}")
        
        data = {
            "device_id": f"ESP32_TEST_{i}",
            "danger": case["danger"],
            "latitude": 20.9517,
            "longitude": 75.1681,
            "location_name": f"Test Pool {i}",
            "wifi_rssi": -50 - i,
            "uptime": 10000 + (i * 1000),
            "timestamp": int(time.time() * 1000),
            "test": True,
            "free_heap": 230000 - (i * 1000),
            "chip_id": f"test_chip_{i}"
        }
        
        try:
            response = requests.post(
                "http://localhost:8000/api/alert",
                json=data,
                headers={"Content-Type": "application/json", "User-Agent": "ESP32HTTPClient/1.0"},
                timeout=5
            )
            print(f"   Response: {response.status_code}")
        except Exception as e:
            print(f"   Error: {e}")
        
        time.sleep(1)  # Wait 1 second between requests

if __name__ == "__main__":
    print("🚨 BACKEND DEBUG LOG TESTER")
    print("=" * 50)
    print("This will send data to your backend to test debug logging")
    print("Make sure your backend is running!")
    print()
    
    # Test single request
    test_backend_logging()
    
    # Ask for multiple tests
    print("\n" + "=" * 50)
    choice = input("Send multiple test requests? (y/n): ").lower().strip()
    if choice in ['y', 'yes']:
        test_multiple_requests()
    
    print("\n🎯 WHAT TO CHECK:")
    print("=" * 50)
    print("1. Your backend terminal should show detailed ESP32 logs")
    print("2. Each request should display:")
    print("   📡 ESP32 COMMUNICATION RECEIVED")
    print("   📱 Device ID and location")
    print("   🚨 Danger status")
    print("   📶 WiFi signal strength")
    print("   ⏱️  Device uptime")
    print("   📊 Additional fields")
    print("3. If no logs appear, the backend might be auto-reloading")
    print("4. Try running: python run_backend_stable.py")