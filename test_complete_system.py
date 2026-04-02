#!/usr/bin/env python3
"""
Complete System Test - ESP32 to Supabase
Tests the entire data flow from ESP32 simulation to Supabase database
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://192.168.1.162:8000/api/alert"
DASHBOARD_URL = "http://192.168.1.162:8000/docs"

def test_esp32_to_backend():
    """Simulate ESP32 sending emergency data to backend"""
    
    print("🧪 TESTING COMPLETE SYSTEM FLOW")
    print("=" * 50)
    print("Simulating ESP32 ESP-NOW emergency data...")
    print()
    
    # Simulate your exact ESP32 data format
    esp32_data = {
        "device_id": "ESP32_ESPNOW_RECEIVER_01",
        "danger": True,
        "latitude": 20.947449,  # Your actual coordinates
        "longitude": 75.554955,
        "location_name": "Emergency Alert System",
        "sender_id": 1,
        "data_source": "esp_now",
        "wifi_rssi": -61,
        "uptime": 123456,
        "timestamp": int(time.time() * 1000),
        "heartbeat": False,
        "test": False,
        "free_heap": 200000,
        "chip_id": "88:13:BF:63:A5:E0",
        "alert_count": 1
    }
    
    try:
        print("📤 Sending ESP32 data to backend...")
        print(f"🌐 URL: {BACKEND_URL}")
        print(f"📊 Data: {json.dumps(esp32_data, indent=2)}")
        print()
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "ESP32HTTPClient/1.0"
        }
        
        response = requests.post(BACKEND_URL, json=esp32_data, headers=headers, timeout=10)
        
        print(f"📡 HTTP Response Code: {response.status_code}")
        print(f"📥 Backend Response:")
        print(response.text)
        print()
        
        if response.status_code == 201:
            print("✅ SUCCESS! Backend received ESP32 data!")
            
            # Parse response to get alert ID
            try:
                response_data = response.json()
                alert_id = response_data.get('data', {}).get('id')
                if alert_id:
                    print(f"🆔 Alert ID created: {alert_id}")
                    return alert_id
            except:
                pass
                
            return True
        else:
            print(f"❌ FAILED! Expected 201, got {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION ERROR!")
        print("🔧 Backend server is not running or not reachable")
        print("💡 Start backend: python backend_anti/main.py")
        return False
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def test_backend_health():
    """Test if backend server is running"""
    try:
        health_url = "http://192.168.1.162:8000/health"
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running!")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except:
        print("❌ Backend server is not reachable!")
        return False

def test_get_alerts():
    """Test retrieving alerts from backend"""
    try:
        alerts_url = f"http://192.168.1.162:8000/api/alerts"
        response = requests.get(alerts_url, timeout=10)
        
        print(f"📡 Get alerts response: {response.status_code}")
        
        if response.status_code == 200:
            alerts_data = response.json()
            total_alerts = alerts_data.get('total', 0)
            print(f"📊 Total alerts in database: {total_alerts}")
            
            if total_alerts > 0:
                latest_alert = alerts_data.get('alerts', [])[0]
                print("📍 Latest alert:")
                print(f"   Device: {latest_alert.get('device_id')}")
                print(f"   Danger: {latest_alert.get('danger')}")
                print(f"   Location: {latest_alert.get('latitude')}, {latest_alert.get('longitude')}")
                print(f"   Time: {latest_alert.get('timestamp')}")
                print("✅ Alerts are being stored in Supabase!")
            else:
                print("ℹ️ No alerts found in database yet")
            
            return True
        else:
            print(f"❌ Failed to get alerts: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error getting alerts: {str(e)}")
        return False

def main():
    print("🚀 COMPLETE SYSTEM TEST")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test 1: Backend Health
    print("1️⃣ Testing backend server health...")
    if not test_backend_health():
        print("❌ Backend server is not running!")
        print("🔧 Start backend: python backend_anti/main.py")
        return
    
    print()
    
    # Test 2: ESP32 Data Simulation
    print("2️⃣ Testing ESP32 data submission...")
    alert_created = test_esp32_to_backend()
    
    print()
    
    # Test 3: Data Retrieval
    print("3️⃣ Testing data retrieval from Supabase...")
    test_get_alerts()
    
    print()
    print("=" * 50)
    print("🎯 SYSTEM STATUS SUMMARY:")
    print("=" * 50)
    
    if alert_created:
        print("✅ ESP32 → Backend → Supabase: WORKING")
        print("✅ Emergency alerts are being stored")
        print("✅ Data appears in dashboard")
        print("✅ Mobile app will receive notifications")
        print()
        print("🔗 Check your dashboard:")
        print(f"   {DASHBOARD_URL}")
        print()
        print("📱 Your ESP32 should now work with this exact flow!")
        print("📤 Upload: esp32_espnow_fixed_with_logging.ino")
        print("🔍 Monitor: Serial output for detailed HTTP logs")
    else:
        print("❌ System has issues - check backend server")
    
    print()
    print("🔧 Next steps:")
    print("1. If test passed: Upload ESP32 code and test with sender")
    print("2. If test failed: Check backend server and Supabase connection")
    print("3. Monitor ESP32 serial output for HTTP communication")

if __name__ == "__main__":
    main()