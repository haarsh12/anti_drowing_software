#!/usr/bin/env python3
"""
ESP32 Communication Test Script
Simulates ESP32 sending various types of data to test backend debugging
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_esp32_communication():
    """Test various ESP32 communication scenarios"""
    
    print("🧪 ESP32 COMMUNICATION DEBUG TEST")
    print("=" * 60)
    print("This script simulates ESP32 sending different types of data")
    print("Check your backend terminal for detailed debug logs!")
    print()
    
    # Test scenarios
    test_scenarios = [
        {
            "name": "🚨 Emergency Alert",
            "description": "Simulates drowning detection emergency",
            "data": {
                "device_id": "ESP32_POOL_MAIN",
                "danger": True,
                "latitude": 20.9517,
                "longitude": 75.1681,
                "location_name": "Jalgaon Main Swimming Pool",
                "rssi": -67,
                "wifi_rssi": -45,
                "uptime": 123456,
                "timestamp": int(time.time() * 1000),
                "temperature": 28.5,
                "humidity": 65.2
            }
        },
        {
            "name": "✅ Safe Status",
            "description": "Normal safe status update",
            "data": {
                "device_id": "ESP32_POOL_MAIN",
                "danger": False,
                "latitude": 20.9517,
                "longitude": 75.1681,
                "location_name": "Jalgaon Main Swimming Pool",
                "rssi": -65,
                "wifi_rssi": -42,
                "uptime": 125000,
                "timestamp": int(time.time() * 1000)
            }
        },
        {
            "name": "💓 Heartbeat",
            "description": "Regular heartbeat message",
            "data": {
                "device_id": "ESP32_POOL_MAIN",
                "danger": False,
                "latitude": 20.9517,
                "longitude": 75.1681,
                "location_name": "Jalgaon Main Swimming Pool",
                "heartbeat": True,
                "wifi_rssi": -48,
                "uptime": 127000,
                "nrf_status": "active",
                "battery_level": 85
            }
        },
        {
            "name": "🧪 Test Message",
            "description": "System test message",
            "data": {
                "device_id": "ESP32_TEST_DEVICE",
                "danger": False,
                "latitude": 20.9520,
                "longitude": 75.1685,
                "location_name": "Test Pool Area",
                "test": True,
                "wifi_rssi": -50,
                "uptime": 5000,
                "nrf_status": "testing"
            }
        },
        {
            "name": "📻 NRF Communication",
            "description": "NRF24L01 receiver data",
            "data": {
                "device_id": "ESP32_NRF_RECEIVER_01",
                "danger": True,
                "latitude": 20.9515,
                "longitude": 75.1675,
                "location_name": "Kids Swimming Pool",
                "wifi_rssi": -52,
                "uptime": 89000,
                "nrf_status": "active",
                "timestamp": int(time.time() * 1000)
            }
        }
    ]
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"📡 Test {i}/5: {scenario['name']}")
        print(f"📝 Description: {scenario['description']}")
        print(f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/alert",
                json=scenario['data'],
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'ESP32HTTPClient/1.0'  # Simulate ESP32 user agent
                },
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"✅ Success: {response.status_code}")
                print(f"📊 Response: {result.get('message', 'OK')}")
                if 'data' in result and 'id' in result['data']:
                    print(f"🆔 Alert ID: {result['data']['id']}")
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"📄 Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)
        
        # Wait between tests to see logs clearly
        if i < len(test_scenarios):
            print("⏳ Waiting 3 seconds before next test...")
            time.sleep(3)
            print()
    
    print("🎉 ESP32 Communication Test Completed!")
    print("=" * 60)
    print("Check your backend terminal for detailed debug information:")
    print("• Device information")
    print("• Signal strength data")
    print("• Emergency vs safe status")
    print("• Heartbeat messages")
    print("• Test mode indicators")
    print("• NRF24L01 status")
    print("• All additional ESP32 fields")

def test_rapid_fire():
    """Test rapid ESP32 communications"""
    print("\n🔥 RAPID FIRE TEST")
    print("=" * 40)
    print("Simulating rapid ESP32 emergency alerts...")
    
    for i in range(5):
        data = {
            "device_id": f"ESP32_RAPID_{i+1}",
            "danger": True,
            "latitude": 20.9517 + (i * 0.001),
            "longitude": 75.1681 + (i * 0.001),
            "location_name": f"Emergency Location {i+1}",
            "rssi": -60 - i,
            "wifi_rssi": -40 - i,
            "uptime": 10000 + (i * 1000),
            "timestamp": int(time.time() * 1000)
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/alert",
                json=data,
                headers={'User-Agent': 'ESP32HTTPClient/1.0'},
                timeout=5
            )
            print(f"📡 Alert {i+1}: {response.status_code}")
        except Exception as e:
            print(f"❌ Alert {i+1} failed: {e}")
        
        time.sleep(0.5)  # 500ms between alerts
    
    print("✅ Rapid fire test completed!")

def main():
    print("🚨 ESP32 BACKEND DEBUGGING TEST SUITE")
    print("=" * 60)
    print("This script helps test ESP32 communication debugging")
    print("Make sure your backend is running: python backend_anti/main.py")
    print()
    
    # Test backend connection first
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running")
            print()
        else:
            print("❌ Backend server responded with error")
            return
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("Please start the backend server first!")
        return
    
    # Run main communication test
    test_esp32_communication()
    
    # Ask if user wants rapid fire test
    print("\n" + "="*60)
    choice = input("Run rapid fire test? (y/n): ").lower().strip()
    if choice in ['y', 'yes']:
        test_rapid_fire()
    
    print("\n🎯 DEBUGGING TIPS:")
    print("=" * 60)
    print("1. Watch backend terminal for detailed ESP32 logs")
    print("2. Each ESP32 communication shows:")
    print("   • Device ID and location")
    print("   • Danger status (emergency vs safe)")
    print("   • Signal strength (RSSI, WiFi)")
    print("   • Device uptime and timestamps")
    print("   • Additional sensor data")
    print("3. Use this data to debug ESP32 connectivity issues")
    print("4. Check for missing fields or incorrect values")

if __name__ == "__main__":
    main()