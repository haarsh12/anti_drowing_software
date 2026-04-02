#!/usr/bin/env python3
"""
Simulate ESP32 Emergency Alert
This script simulates a real ESP32 device sending emergency data to the backend
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000/api/alert"

def simulate_esp32_emergency():
    """Simulate a real ESP32 emergency alert"""
    
    print("🚨 SIMULATING ESP32 EMERGENCY ALERT")
    print("=" * 50)
    
    # Real emergency coordinates (example: Central Park, NYC)
    emergency_data = {
        "device_id": "ESP32_EMERGENCY_DEVICE_01",
        "danger": True,  # RED EMERGENCY ALERT
        "latitude": 40.785091,  # Central Park coordinates
        "longitude": -73.968285,
        "location_name": "Central Park Lake - Emergency Zone",
        
        # ESP32 specific fields (what real ESP32 would send)
        "wifi_rssi": -42,
        "uptime": 156789,  # Device uptime in milliseconds
        "timestamp": int(time.time() * 1000),  # Current timestamp
        "heartbeat": False,  # This is NOT a heartbeat - it's a real emergency
        "test": False,  # This is NOT a test - it's a real emergency
        "free_heap": 234567,
        "chip_id": "240AC4A1B2C8",
        "data_source": "esp_now",
        "sender_id": 12345,
        "alert_count": 1
    }
    
    print("📊 EMERGENCY DATA TO SEND:")
    print("-" * 30)
    for key, value in emergency_data.items():
        if key in ["latitude", "longitude"]:
            print(f"{key}: {value:.6f}")
        else:
            print(f"{key}: {value}")
    print("-" * 30)
    
    # Send the emergency alert
    print("\n🚀 SENDING EMERGENCY ALERT TO BACKEND...")
    print(f"📡 URL: {BACKEND_URL}")
    
    try:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "ESP32HTTPClient/1.0"  # Simulate ESP32 user agent
        }
        
        response = requests.post(
            BACKEND_URL,
            json=emergency_data,
            headers=headers,
            timeout=10
        )
        
        print(f"\n📡 HTTP RESPONSE CODE: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ SUCCESS! EMERGENCY ALERT CREATED!")
            print("=" * 50)
            
            response_data = response.json()
            print("📊 BACKEND RESPONSE:")
            print(json.dumps(response_data, indent=2))
            
            print("\n🎯 WHAT HAPPENED:")
            print("• RED emergency alert created in database")
            print("• Alert will appear on dashboard immediately")
            print("• Frontend will show red marker on map")
            print("• Mobile app will receive push notification")
            print("• Guards will be alerted for immediate response")
            
            print(f"\n📍 EMERGENCY LOCATION:")
            print(f"• Coordinates: {emergency_data['latitude']:.6f}, {emergency_data['longitude']:.6f}")
            print(f"• Location: {emergency_data['location_name']}")
            print(f"• Device: {emergency_data['device_id']}")
            
            print(f"\n🔗 CHECK RESULTS:")
            print("• Dashboard: http://localhost:8000/docs")
            print("• API Alerts: http://localhost:8000/api/alerts")
            print("• Frontend: Check your React dashboard")
            
            return True
            
        else:
            print(f"❌ FAILED! Response code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ REQUEST FAILED: {e}")
        print("\n🔧 TROUBLESHOOTING:")
        print("• Make sure backend is running: python backend_anti/main.py")
        print("• Check if port 8000 is accessible")
        print("• Verify backend URL is correct")
        return False

def check_alert_in_database():
    """Check if the alert appears in the database"""
    print("\n🔍 VERIFYING ALERT IN DATABASE...")
    
    try:
        response = requests.get("http://localhost:8000/api/alerts/latest", timeout=5)
        
        if response.status_code == 200:
            alert = response.json()
            print("✅ LATEST ALERT FOUND:")
            print(f"• Device: {alert.get('device_id')}")
            print(f"• Status: {'🔴 EMERGENCY' if alert.get('danger') else '🟢 SAFE'}")
            print(f"• Location: {alert.get('location_name')}")
            print(f"• Time: {alert.get('timestamp')}")
            return True
        else:
            print(f"❌ Could not fetch latest alert: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking database: {e}")
        return False

def main():
    """Main simulation function"""
    print("🚨 ESP32 EMERGENCY SIMULATION")
    print("=" * 50)
    print("This simulates what a real ESP32 would send during an emergency")
    print()
    
    # Send the emergency alert
    success = simulate_esp32_emergency()
    
    if success:
        # Wait a moment then check database
        time.sleep(1)
        check_alert_in_database()
        
        print("\n" + "=" * 50)
        print("✅ ESP32 EMERGENCY SIMULATION COMPLETE")
        print("=" * 50)
        print("\n🎯 NEXT STEPS:")
        print("1. Check your frontend dashboard - you should see a RED alert")
        print("2. The alert should appear on the map at Central Park coordinates")
        print("3. Mobile app should receive emergency notification")
        print("4. This alert requires guard response/acceptance")
        print("\n💡 This is exactly what would happen with a real ESP32!")
        
    else:
        print("\n❌ SIMULATION FAILED")
        print("Please check your backend is running and try again")

if __name__ == "__main__":
    main()