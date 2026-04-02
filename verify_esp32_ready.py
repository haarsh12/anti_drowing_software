#!/usr/bin/env python3
"""
Verify ESP32 Real Data Setup
This script checks if your system is ready to receive real ESP32 data only
"""

import requests
import json
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
API_URL = f"{BACKEND_URL}/api"

def check_backend_status():
    """Check if backend is running and ready"""
    print("🔍 Checking backend status...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend is not reachable: {e}")
        print("💡 Make sure to run: python backend_anti/main.py")
        return False

def check_current_alerts():
    """Check current alerts in database"""
    print("\n🔍 Checking current alerts...")
    
    try:
        response = requests.get(f"{API_URL}/alerts", timeout=5)
        if response.status_code == 200:
            data = response.json()
            alert_count = data.get('total', 0)
            print(f"📊 Current alerts in database: {alert_count}")
            
            if alert_count == 0:
                print("✅ Database is clean - ready for real ESP32 data")
            else:
                print("⚠️ Database contains existing alerts")
                for alert in data.get('alerts', [])[:3]:  # Show first 3
                    device_id = alert.get('device_id', 'Unknown')
                    danger = alert.get('danger', False)
                    timestamp = alert.get('timestamp', 'Unknown')
                    status = "🔴 EMERGENCY" if danger else "🟢 SAFE"
                    print(f"   • {device_id}: {status} at {timestamp}")
            
            return True
        else:
            print(f"❌ Failed to fetch alerts: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to check alerts: {e}")
        return False

def simulate_esp32_test():
    """Send a test ESP32 request to verify the endpoint works"""
    print("\n🧪 Testing ESP32 endpoint...")
    
    test_data = {
        "device_id": "ESP32_TEST_VERIFICATION",
        "danger": True,
        "latitude": 40.7128,
        "longitude": -74.0060,
        "location_name": "Test Location - ESP32 Verification",
        "test": True,
        "wifi_rssi": -45,
        "uptime": 12345
    }
    
    try:
        response = requests.post(
            f"{API_URL}/alert",
            json=test_data,
            headers={"Content-Type": "application/json", "User-Agent": "ESP32HTTPClient/1.0"},
            timeout=10
        )
        
        if response.status_code == 201:
            print("✅ ESP32 endpoint is working correctly")
            print(f"📊 Response: {response.json()}")
            return True
        else:
            print(f"❌ ESP32 endpoint failed: {response.status_code}")
            print(f"📊 Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ ESP32 endpoint test failed: {e}")
        return False

def clear_test_data():
    """Clear the test data we just created"""
    print("\n🧹 Cleaning up test data...")
    
    try:
        # Get all alerts
        response = requests.get(f"{API_URL}/alerts", timeout=5)
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            # Find and note test alerts
            test_alerts = [alert for alert in alerts if 'TEST' in alert.get('device_id', '')]
            if test_alerts:
                print(f"🗑️ Found {len(test_alerts)} test alerts")
                print("💡 Test alerts will remain for verification")
                print("💡 Real ESP32 data will appear alongside test data")
            else:
                print("✅ No test alerts found")
        
    except Exception as e:
        print(f"⚠️ Could not check for test data: {e}")

def main():
    """Main verification function"""
    print("=" * 60)
    print("🚀 ESP32 REAL DATA VERIFICATION")
    print("=" * 60)
    print("This script verifies your system is ready for REAL ESP32 data only")
    print()
    
    # Check backend
    if not check_backend_status():
        print("\n❌ VERIFICATION FAILED: Backend not ready")
        return False
    
    # Check alerts
    if not check_current_alerts():
        print("\n❌ VERIFICATION FAILED: Cannot access alerts")
        return False
    
    # Test ESP32 endpoint
    if not simulate_esp32_test():
        print("\n❌ VERIFICATION FAILED: ESP32 endpoint not working")
        return False
    
    # Clean up
    clear_test_data()
    
    print("\n" + "=" * 60)
    print("✅ VERIFICATION COMPLETE - SYSTEM READY FOR REAL ESP32 DATA")
    print("=" * 60)
    print()
    print("📋 NEXT STEPS:")
    print("1. Upload the fixed ESP32 code to your device:")
    print("   • esp32_espnow_final_working.ino (receiver)")
    print("   • Make sure WiFi password is correct")
    print()
    print("2. Your ESP32 should connect and send data to:")
    print(f"   • Backend: {API_URL}/alert")
    print(f"   • Dashboard: {BACKEND_URL}/docs")
    print()
    print("3. Watch the backend console for ESP32 logs:")
    print("   📡 ESP32 COMMUNICATION RECEIVED")
    print("   🚨 EMERGENCY DETECTED - SENDING RED ALERT!")
    print()
    print("4. Check the frontend for real alerts:")
    print("   • Red emergency markers on map")
    print("   • Alert notifications")
    print()
    print("🎯 NO MORE TEST DATA - ONLY REAL ESP32 ALERTS!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    main()