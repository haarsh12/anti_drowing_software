#!/usr/bin/env python3
"""
Quick Emergency Test
===================
Sends a single emergency alert to test the system quickly.
"""

import requests
import json
import time
from datetime import datetime

def send_emergency_alert():
    """Send a single emergency alert for testing"""
    
    print("🚨 QUICK EMERGENCY TEST")
    print("=" * 30)
    
    # Backend URL
    backend_url = "http://127.0.0.1:8000"
    
    # Test data
    alert_data = {
        "device_id": f"QUICK_TEST_{int(time.time())}",
        "danger": True,
        "latitude": 40.7128,  # NYC coordinates
        "longitude": -74.0060
    }
    
    print(f"📡 Sending emergency alert...")
    print(f"   Device: {alert_data['device_id']}")
    print(f"   Location: {alert_data['latitude']}, {alert_data['longitude']}")
    print(f"   Danger: {'🚨 YES' if alert_data['danger'] else '✅ NO'}")
    
    try:
        # Send the alert
        response = requests.post(
            f"{backend_url}/api/alert",
            json=alert_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 201:
            result = response.json()
            print(f"✅ SUCCESS! Alert sent successfully!")
            print(f"   Alert ID: {result.get('alert_id')}")
            print(f"   Message: {result.get('message')}")
            
            print("\n🔍 What to check now:")
            print("   1. 🌐 Web Dashboard: http://localhost:3000")
            print("   2. 📱 Mobile App: Should show new alert")
            print("   3. 🖥️  Backend API: http://127.0.0.1:8000/api/alerts")
            
            return True
            
        else:
            print(f"❌ FAILED! Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR!")
        print("   Make sure your backend is running:")
        print("   cd backend_anti")
        print("   python -m uvicorn main:app --reload")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    send_emergency_alert()
    
    print("\n" + "=" * 30)
    input("Press Enter to exit...")