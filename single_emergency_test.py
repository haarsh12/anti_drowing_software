#!/usr/bin/env python3
"""
Single Emergency Test
====================
Sends ONE emergency alert to test the perfect notification system.
"""

import requests
import json
import time
from datetime import datetime

def send_single_emergency():
    """Send a single emergency alert for testing"""
    
    print("🚨 SINGLE EMERGENCY TEST")
    print("=" * 40)
    
    # Backend URL
    backend_url = "http://127.0.0.1:8000"
    
    # Single test case - Jalgaon Railway Station
    alert_data = {
        "device_id": "EMERGENCY_TEST_JALGAON_STATION",
        "danger": True,
        "latitude": 20.947409,  # Exact Jalgaon Railway Station coordinates
        "longitude": 75.554987
    }
    
    print(f"📡 Sending SINGLE emergency alert...")
    print(f"   Device: {alert_data['device_id']}")
    print(f"   Location: Jalgaon Railway Station")
    print(f"   Coordinates: {alert_data['latitude']}, {alert_data['longitude']}")
    print(f"   Status: 🚨 DANGER - IMMEDIATE RESPONSE REQUIRED")
    print()
    
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
            print(f"✅ SUCCESS! Emergency alert sent successfully!")
            print(f"   Alert ID: {result.get('alert_id')}")
            print(f"   Message: {result.get('message')}")
            print()
            
            print("🔍 WHAT SHOULD HAPPEN NOW:")
            print("=" * 40)
            print("1. 📱 MOBILE APP:")
            print("   → Full-screen emergency notification appears IMMEDIATELY")
            print("   → Works even if phone is locked or in other apps")
            print("   → Shows premium white design with action buttons")
            print("   → Cannot be dismissed until action is taken")
            print()
            print("2. 🌐 WEB DASHBOARD:")
            print("   → Red marker appears on Jalgaon map")
            print("   → Shows at Jalgaon Railway Station location")
            print("   → Updates in real-time")
            print()
            print("3. 🗺️ MAP FEATURES:")
            print("   → Map centers on Jalgaon, Maharashtra")
            print("   → Red marker for this emergency")
            print("   → Interactive popup with case details")
            print()
            print("4. 👥 GUARD RESPONSES:")
            print("   → When guards respond, all others see the action")
            print("   → Real-time updates of who responded")
            print("   → Complete guard coordination")
            print()
            
            print("🎯 TEST CHECKLIST:")
            print("=" * 40)
            print("□ Mobile notification appears within 3 seconds")
            print("□ Notification works outside the app")
            print("□ Premium white design with 4 buttons")
            print("□ Google Maps button opens exact location")
            print("□ Web dashboard shows red marker")
            print("□ Map is centered on Jalgaon")
            print("□ Guard responses are tracked")
            
            return True
            
        else:
            print(f"❌ FAILED! Status code: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR!")
        print("   Make sure your backend is running:")
        print("   cd backend_anti")
        print("   run_server.bat")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    print("🎯 PERFECT EMERGENCY NOTIFICATION TEST")
    print("Testing system-level notifications with premium design")
    print()
    
    success = send_single_emergency()
    
    if success:
        print("\n" + "=" * 40)
        print("✅ TEST COMPLETED SUCCESSFULLY!")
        print("Check your mobile app and web dashboard now.")
    else:
        print("\n" + "=" * 40)
        print("❌ TEST FAILED!")
        print("Please check your backend connection.")
    
    input("\nPress Enter to exit...")