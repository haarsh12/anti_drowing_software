#!/usr/bin/env python3
"""
Test exact ESP32 request to debug 500 error
"""

import requests
import json

def test_exact_esp32_request():
    """Test the exact same request ESP32 is sending"""
    
    url = "http://localhost:8000/api/alert"
    
    # Exact same data ESP32 is sending
    data = {
        "device_id": "ESP32_DEBUG_01",
        "danger": True,
        "latitude": 20.9517,
        "longitude": 75.1681,
        "timestamp": 10087
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    print("🧪 Testing exact ESP32 request...")
    print(f"URL: {url}")
    print(f"Data: {json.dumps(data, indent=2)}")
    print(f"Headers: {headers}")
    print()
    
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 500:
            print("\n❌ 500 Internal Server Error detected!")
            print("This means the backend received the request but failed to process it.")
            print("Check the backend terminal for error details.")
        
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_exact_esp32_request()