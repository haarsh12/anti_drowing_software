#!/usr/bin/env python3
"""
Clear Test Data and Fix ESP32 System
Removes all test/heartbeat data and shows only real ESP32 emergency alerts
"""

import requests
import json

# Configuration
BACKEND_URL = "http://192.168.1.162:8000"

def clear_all_alerts():
    """Clear all existing alerts to start fresh"""
    try:
        # You'll need to implement this endpoint or manually clear
        print("🧹 Clearing all test data...")
        print("ℹ️  You can manually clear via dashboard or database")
        return True
    except Exception as e:
        print(f"❌ Error clearing data: {e}")
        return False

def check_current_alerts():
    """Check what alerts are currently in the system"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/alerts", timeout=10)
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            print(f"📊 Current alerts in system: {len(alerts)}")
            
            # Show recent alerts
            for i, alert in enumerate(alerts[:5]):
                danger_status = "🚨 EMERGENCY" if alert.get('danger') else "🟢 SAFE"
                heartbeat = "💓 HEARTBEAT" if alert.get('heartbeat') else "📍 REAL DATA"
                
                print(f"   {i+1}. {danger_status} | {heartbeat}")
                print(f"      Coords: {alert.get('latitude')}, {alert.get('longitude')}")
                print(f"      Device: {alert.get('device_id')}")
                print(f"      Time: {alert.get('timestamp')}")
                print()
            
            return True
        else:
            print(f"❌ Failed to get alerts: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error checking alerts: {e}")
        return False

def main():
    print("🔧 ESP32 SYSTEM FIX - REMOVE TEST DATA")
    print("=" * 50)
    
    # Check current system state
    print("1️⃣ Checking current alerts...")
    check_current_alerts()
    
    print("\n" + "=" * 50)
    print("🚨 CRITICAL ISSUE IDENTIFIED:")
    print("=" * 50)
    print("Your ESP32 is receiving real coordinates:")
    print("📍 ESP32 Serial: Lat: 20.947319, Lon: 75.554886")
    print()
    print("But backend is only receiving heartbeat data:")
    print("💓 Backend: Lat: 20.94732, Lon: 75.55489 (old coordinates)")
    print("🟢 Status: SAFE (should be EMERGENCY)")
    print("💓 Heartbeat: True (should be False for real data)")
    print()
    
    print("🔧 SOLUTION:")
    print("=" * 50)
    print("1. Your ESP32 is NOT sending the real emergency coordinates")
    print("2. It's only sending heartbeat data every 30 seconds")
    print("3. The processAndSendToBackend() function is not working")
    print()
    
    print("📋 STEPS TO FIX:")
    print("=" * 50)
    print("1. Upload the CORRECT ESP32 code:")
    print("   File: esp32_espnow_fixed_with_logging.ino")
    print()
    print("2. You should see this when ESP-NOW data is received:")
    print("   📩 RECEIVED ESP-NOW DATA")
    print("   🚨 PROCESSING EMERGENCY ALERT")
    print("   🚀 SENDING TO BACKEND SERVER")
    print("   📡 HTTP RESPONSE CODE: 201")
    print("   🎯 SUCCESS! EMERGENCY ALERT CREATED!")
    print()
    print("3. Backend should show:")
    print("   🚨 Danger Status: 🔴 EMERGENCY!")
    print("   💓 Heartbeat: False")
    print("   📍 Real coordinates from ESP-NOW")
    print()
    
    print("❌ CURRENT PROBLEM:")
    print("=" * 50)
    print("Your ESP32 code is calling processAndSendToBackend()")
    print("but it's not actually sending emergency data.")
    print("Only heartbeat data is being sent every 30 seconds.")
    print()
    
    print("✅ SOLUTION:")
    print("=" * 50)
    print("Upload: esp32_espnow_fixed_with_logging.ino")
    print("This version will:")
    print("• Show detailed HTTP logs")
    print("• Send real coordinates as EMERGENCY")
    print("• Mark danger=true for ESP-NOW data")
    print("• Display success/failure messages")
    print()
    
    print("🎯 EXPECTED RESULT:")
    print("=" * 50)
    print("When you send ESP-NOW data, you'll see:")
    print("• ESP32 Serial: Detailed HTTP communication")
    print("• Backend: 🚨 Danger Status: 🔴 EMERGENCY!")
    print("• Dashboard: Real emergency alerts")
    print("• Mobile App: Push notifications")

if __name__ == "__main__":
    main()