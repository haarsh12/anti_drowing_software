#!/usr/bin/env python3
"""
Test Full-Screen Emergency Notifications
Creates emergency alerts specifically to test mobile app full-screen notifications
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_full_screen_notifications():
    """Test full-screen emergency notifications"""
    
    print("🚨 TESTING FULL-SCREEN EMERGENCY NOTIFICATIONS")
    print("=" * 60)
    print("This test creates emergency alerts to trigger full-screen overlays")
    print("Make sure your mobile app is running and logged in!")
    print()
    
    # Test emergency data
    emergency_alerts = [
        {
            "device_id": "ESP32_POOL_MAIN",
            "danger": True,
            "latitude": 20.9517,
            "longitude": 75.1681,
            "location_name": "Main Swimming Pool - EMERGENCY"
        },
        {
            "device_id": "ESP32_POOL_KIDS", 
            "danger": True,
            "latitude": 20.9520,
            "longitude": 75.1685,
            "location_name": "Kids Pool - EMERGENCY"
        }
    ]
    
    created_alerts = []
    
    for i, alert_data in enumerate(emergency_alerts, 1):
        print(f"🚨 Creating Emergency Alert {i}/2...")
        print(f"📍 Location: {alert_data['location_name']}")
        print(f"📱 Device: {alert_data['device_id']}")
        print(f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/alert",
                json=alert_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                alert_response = response.json()
                alert_id = None
                
                # Extract alert ID properly
                if "data" in alert_response:
                    alert_id = alert_response["data"].get("id") or alert_response["data"].get("alert_id")
                if not alert_id:
                    alert_id = alert_response.get("id") or alert_response.get("alert_id")
                
                created_alerts.append({
                    'id': alert_id,
                    'device_id': alert_data['device_id'],
                    'location': alert_data['location_name']
                })
                
                print(f"✅ Emergency Alert {i} Created Successfully!")
                print(f"🆔 Alert ID: {alert_id}")
                print(f"📊 Response: {alert_response.get('message', 'Success')}")
                print()
                
                # Wait 3 seconds for mobile app to detect
                print("⏳ Waiting 3 seconds for mobile app to detect...")
                time.sleep(3)
                
            else:
                print(f"❌ Alert {i} failed: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Alert {i} error: {e}")
        
        print("-" * 40)
    
    # Summary
    print("\n📊 FULL-SCREEN NOTIFICATION TEST SUMMARY")
    print("=" * 60)
    
    if created_alerts:
        print(f"✅ Created {len(created_alerts)} emergency alerts")
        print("\n📱 Your mobile app should now show:")
        print("  🔔 System-level notifications (even if app is closed)")
        print("  📺 Full-screen emergency overlays with red background")
        print("  🎯 Action buttons: Accept, Complete, Not Available")
        print("  📍 Google Maps integration")
        print("  📳 Intense vibration patterns")
        print("  🚨 Emergency case information")
        
        print("\n🧪 Test Each Alert:")
        for i, alert in enumerate(created_alerts, 1):
            print(f"  {i}. Alert ID: {alert['id']} - {alert['location']}")
            print(f"     Device: {alert['device_id']}")
        
        print("\n✅ Expected Mobile App Behavior:")
        print("  1. Full-screen overlay appears immediately")
        print("  2. Red emergency background with pulsing animation")
        print("  3. Case ID and location information displayed")
        print("  4. Three action buttons are functional")
        print("  5. Google Maps button opens location")
        print("  6. Overlay cannot be dismissed without action")
        print("  7. Vibration feedback on all interactions")
        
        print("\n🔧 If notifications don't appear:")
        print("  1. Check mobile app is connected to backend")
        print("  2. Verify notification permissions are granted")
        print("  3. Ensure app is logged in with guard account")
        print("  4. Check notification service is polling (every 3 seconds)")
        print("  5. Verify backend is running on correct IP address")
        
    else:
        print("❌ No alerts were created successfully")
        print("Please check backend connection and try again")
    
    return len(created_alerts) > 0

def main():
    print("🧪 FULL-SCREEN EMERGENCY NOTIFICATION TEST")
    print("=" * 60)
    print("This test specifically targets the full-screen overlay feature")
    print("Make sure your mobile app is:")
    print("  • Running and logged in")
    print("  • Connected to the backend")
    print("  • Has notification permissions enabled")
    print()
    
    success = test_full_screen_notifications()
    
    print("\n" + "="*60)
    if success:
        print("🎉 FULL-SCREEN NOTIFICATION TEST COMPLETED!")
        print("Check your mobile app for emergency overlays")
    else:
        print("❌ FULL-SCREEN NOTIFICATION TEST FAILED")
        print("Please check backend connection and mobile app setup")
    print("="*60)

if __name__ == "__main__":
    main()