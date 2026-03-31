"""
Verify Supabase integration with the IoT Alert System
"""
import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test all API endpoints"""
    print("🧪 Testing IoT Alert System API with Supabase")
    print("=" * 60)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print(f"   ✅ Health check: {response.json()['status']}")
        else:
            print(f"   ❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    # Test 2: Create danger alert
    print("\n2. Creating danger alert...")
    danger_alert = {
        "device_id": "esp32_danger_test",
        "danger": True,
        "latitude": 18.5204,
        "longitude": 73.8567
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/alert",
            json=danger_alert,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Danger alert created: ID {result['alert_id']}")
        else:
            print(f"   ❌ Failed to create danger alert: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Create danger alert error: {e}")
    
    # Test 3: Create safe alert
    print("\n3. Creating safe alert...")
    safe_alert = {
        "device_id": "esp32_safe_test",
        "danger": False,
        "latitude": 18.5300,
        "longitude": 73.8600
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/alert",
            json=safe_alert,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 201:
            result = response.json()
            print(f"   ✅ Safe alert created: ID {result['alert_id']}")
        else:
            print(f"   ❌ Failed to create safe alert: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Create safe alert error: {e}")
    
    # Test 4: Get all alerts
    print("\n4. Retrieving all alerts...")
    try:
        response = requests.get(f"{BASE_URL}/api/alerts")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Retrieved {data['total']} alerts from Supabase")
            
            # Display recent alerts
            for alert in data['alerts'][:3]:  # Show first 3
                status = "🚨 DANGER" if alert['danger'] else "✅ SAFE"
                timestamp = datetime.fromisoformat(alert['timestamp'].replace('Z', '+00:00'))
                print(f"      {status} | {alert['device_id']} | {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"   ❌ Failed to retrieve alerts: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Retrieve alerts error: {e}")
    
    # Test 5: Get latest alert
    print("\n5. Getting latest alert...")
    try:
        response = requests.get(f"{BASE_URL}/api/alerts/latest")
        if response.status_code == 200:
            alert = response.json()
            status = "🚨 DANGER" if alert['danger'] else "✅ SAFE"
            timestamp = datetime.fromisoformat(alert['timestamp'].replace('Z', '+00:00'))
            print(f"   ✅ Latest alert: {status}")
            print(f"      Device: {alert['device_id']}")
            print(f"      Location: {alert['latitude']}, {alert['longitude']}")
            print(f"      Time: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(f"   ❌ Failed to get latest alert: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Latest alert error: {e}")
    
    # Test 6: Get alerts by device
    print("\n6. Getting alerts by device...")
    try:
        response = requests.get(f"{BASE_URL}/api/alerts/esp32_danger_test")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Found {data['total']} alerts for device 'esp32_danger_test'")
        else:
            print(f"   ❌ Failed to get device alerts: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Device alerts error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Supabase integration test completed!")
    print("Your IoT Alert System is ready to receive data from ESP32 devices.")

if __name__ == "__main__":
    test_api_endpoints()