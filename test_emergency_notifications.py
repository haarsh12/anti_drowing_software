#!/usr/bin/env python3
"""
Test Emergency Notification System
Creates emergency alerts to test mobile app notifications
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def create_emergency_alert():
    """Create an emergency alert to trigger mobile notifications"""
    
    print("🚨 Creating Emergency Alert for Mobile App Testing...")
    print("=" * 60)
    
    # Emergency data
    emergency_data = {
        "device_id": "ESP32_EMERGENCY_TEST",
        "danger": True,
        "latitude": 20.9517,
        "longitude": 75.1681,
        "location_name": "Jalgaon Main Swimming Pool - EMERGENCY TEST"
    }
    
    try:
        print(f"📍 Location: {emergency_data['location_name']}")
        print(f"📱 Device: {emergency_data['device_id']}")
        print(f"🚨 Danger Status: {'YES - EMERGENCY!' if emergency_data['danger'] else 'No'}")
        print(f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        response = requests.post(
            f"{BASE_URL}/api/alert",
            json=emergency_data,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            alert_data = response.json()
            alert_id = alert_data.get("data", {}).get("id")
            
            print("✅ EMERGENCY ALERT CREATED SUCCESSFULLY!")
            print(f"🆔 Alert ID: {alert_id}")
            print(f"📊 Response: {alert_data.get('message', 'Success')}")
            print()
            print("📱 Mobile App Should Now Show:")
            print("  🔔 System notification (even if app is closed)")
            print("  📺 Full-screen emergency overlay")
            print("  🎯 Action buttons: Accept, Complete, Not Available")
            print("  📍 Google Maps integration")
            print("  📳 Vibration and haptic feedback")
            print()
            print("🧪 Test Instructions:")
            print("1. Check your mobile app for notifications")
            print("2. Verify full-screen overlay appears")
            print("3. Test action buttons work")
            print("4. Confirm Google Maps opens correctly")
            print("5. Check case appears in home screen list")
            
            return True
            
        else:
            print(f"❌ Failed to create alert: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error creating alert: {e}")
        return False

def create_multiple_alerts():
    """Create multiple alerts for comprehensive testing"""
    
    print("\n🔥 Creating Multiple Emergency Alerts...")
    print("=" * 60)
    
    alerts = [
        {
            "device_id": "ESP32_POOL_01",
            "danger": True,
            "latitude": 20.9517,
            "longitude": 75.1681,
            "location_name": "Main Swimming Pool"
        },
        {
            "device_id": "ESP32_POOL_02", 
            "danger": True,
            "latitude": 20.9520,
            "longitude": 75.1685,
            "location_name": "Kids Swimming Pool"
        },
        {
            "device_id": "ESP32_POOL_03",
            "danger": True,
            "latitude": 20.9515,
            "longitude": 75.1675,
            "location_name": "Therapy Pool"
        }
    ]
    
    created_count = 0
    
    for i, alert_data in enumerate(alerts, 1):
        print(f"\n🚨 Creating Alert {i}/3...")
        print(f"📍 {alert_data['location_name']}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/alert",
                json=alert_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                created_count += 1
                print(f"✅ Alert {i} created successfully")
            else:
                print(f"❌ Alert {i} failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Alert {i} error: {e}")
        
        # Small delay between alerts
        time.sleep(1)
    
    print(f"\n📊 Summary: {created_count}/3 alerts created")
    print("📱 Mobile app should now show multiple emergency notifications!")
    
    return created_count > 0

def main():
    print("🧪 EMERGENCY NOTIFICATION SYSTEM TEST")
    print("=" * 60)
    print("This test creates emergency alerts to trigger mobile notifications")
    print("Make sure your mobile app is running and connected!")
    print()
    
    # Test 1: Single Emergency Alert
    success1 = create_emergency_alert()
    
    if success1:
        print("\n⏳ Waiting 5 seconds before creating multiple alerts...")
        time.sleep(5)
        
        # Test 2: Multiple Emergency Alerts
        success2 = create_multiple_alerts()
        
        if success2:
            print("\n🎉 EMERGENCY NOTIFICATION TEST COMPLETED!")
            print("=" * 60)
            print("✅ Emergency alerts created successfully")
            print("📱 Check your mobile app for:")
            print("  • System-level notifications")
            print("  • Full-screen emergency overlays") 
            print("  • Action buttons functionality")
            print("  • Case list updates")
            print("  • Google Maps integration")
            print()
            print("🔧 If notifications don't appear:")
            print("  1. Check mobile app is connected to backend")
            print("  2. Verify notification permissions are granted")
            print("  3. Ensure polling service is running")
            print("  4. Check backend logs for errors")
        else:
            print("\n❌ Multiple alerts test failed")
    else:
        print("\n❌ Single alert test failed")
        print("Please check backend connection and try again")

if __name__ == "__main__":
    main()