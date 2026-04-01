#!/usr/bin/env python3
"""
Complete System Test Script
Tests all components of the anti-drowning emergency system
"""

import requests
import json
import time
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TEST_DEVICE_ID = "test_esp32_001"
TEST_COORDINATES = {
    "latitude": 20.9517,
    "longitude": 75.1681
}

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🧪 {title}")
    print(f"{'='*50}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def test_backend_health():
    """Test if backend server is running"""
    print_header("Backend Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/api/alerts", timeout=5)
        if response.status_code == 200:
            print_success("Backend server is running")
            data = response.json()
            print_info(f"Current alerts in system: {data.get('total', 0)}")
            return True
        else:
            print_error(f"Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend server")
        print_info("Make sure backend is running: python backend_anti/main.py")
        return False
    except Exception as e:
        print_error(f"Backend health check failed: {e}")
        return False

def test_user_registration():
    """Test user registration endpoint"""
    print_header("User Registration Test")
    
    test_user = {
        "name": "Test Guard",
        "phone": f"+91{int(time.time()) % 10000000000}",  # Unique phone number
        "password": "test123",
        "role": "guard"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=test_user,
            timeout=10
        )
        
        if response.status_code == 201:
            print_success("User registration successful")
            return test_user
        else:
            print_error(f"Registration failed: {response.text}")
            return None
    except Exception as e:
        print_error(f"Registration test failed: {e}")
        return None

def test_user_login(user_data):
    """Test user login endpoint"""
    print_header("User Login Test")
    
    if not user_data:
        print_error("No user data provided for login test")
        return None
    
    login_data = {
        "phone": user_data["phone"],
        "password": user_data["password"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success("User login successful")
            print_info(f"Token received: {data['access_token'][:20]}...")
            return data['access_token']
        else:
            print_error(f"Login failed: {response.text}")
            return None
    except Exception as e:
        print_error(f"Login test failed: {e}")
        return None

def test_emergency_alert_creation():
    """Test emergency alert creation"""
    print_header("Emergency Alert Creation Test")
    
    # Test danger alert
    danger_alert = {
        "device_id": TEST_DEVICE_ID,
        "danger": True,
        "latitude": TEST_COORDINATES["latitude"],
        "longitude": TEST_COORDINATES["longitude"]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/alert",
            json=danger_alert,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            print_success("Emergency alert created successfully")
            print_info(f"Alert ID: {data.get('id', 'N/A')}")
            return data.get('id')
        else:
            print_error(f"Alert creation failed: {response.text}")
            return None
    except Exception as e:
        print_error(f"Alert creation test failed: {e}")
        return None

def test_guard_response(alert_id, token):
    """Test guard response to alert"""
    print_header("Guard Response Test")
    
    if not alert_id or not token:
        print_error("Missing alert ID or authentication token")
        return False
    
    response_data = {
        "alert_id": alert_id,
        "action": "accepted",
        "notes": "Test response from automated test"
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/guard-response",
            json=response_data,
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print_success("Guard response recorded successfully")
            return True
        else:
            print_error(f"Guard response failed: {response.text}")
            return False
    except Exception as e:
        print_error(f"Guard response test failed: {e}")
        return False

def test_alerts_retrieval():
    """Test alerts retrieval endpoint"""
    print_header("Alerts Retrieval Test")
    
    try:
        response = requests.get(f"{BASE_URL}/api/alerts", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            print_success(f"Retrieved {len(alerts)} alerts")
            
            # Show recent alerts
            if alerts:
                print_info("Recent alerts:")
                for alert in alerts[-3:]:  # Show last 3 alerts
                    danger_status = "🚨 DANGER" if alert.get('danger') else "✅ SAFE"
                    print_info(f"  - ID: {alert.get('id')}, Device: {alert.get('device_id')}, Status: {danger_status}")
            
            return True
        else:
            print_error(f"Alerts retrieval failed: {response.text}")
            return False
    except Exception as e:
        print_error(f"Alerts retrieval test failed: {e}")
        return False

def test_esp32_simulation():
    """Simulate ESP32 sending data"""
    print_header("ESP32 Simulation Test")
    
    print_info("Simulating ESP32 sending emergency data...")
    
    # Simulate heartbeat
    heartbeat_data = {
        "device_id": TEST_DEVICE_ID,
        "danger": False,
        "latitude": 0.0,
        "longitude": 0.0,
        "heartbeat": True,
        "wifi_rssi": -45,
        "uptime": 12345
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/alert",
            json=heartbeat_data,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print_success("ESP32 heartbeat simulation successful")
        else:
            print_error(f"ESP32 heartbeat simulation failed: {response.text}")
            return False
    except Exception as e:
        print_error(f"ESP32 simulation failed: {e}")
        return False
    
    # Simulate emergency
    time.sleep(1)
    emergency_data = {
        "device_id": TEST_DEVICE_ID,
        "danger": True,
        "latitude": TEST_COORDINATES["latitude"],
        "longitude": TEST_COORDINATES["longitude"],
        "rssi": -67,
        "timestamp": int(time.time() * 1000)
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/alert",
            json=emergency_data,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print_success("ESP32 emergency simulation successful")
            return True
        else:
            print_error(f"ESP32 emergency simulation failed: {response.text}")
            return False
    except Exception as e:
        print_error(f"ESP32 emergency simulation failed: {e}")
        return False

def run_complete_test():
    """Run complete system test"""
    print_header("Anti-Drowning Emergency System - Complete Test")
    print_info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_info(f"Backend URL: {BASE_URL}")
    
    test_results = []
    
    # Test 1: Backend Health
    result = test_backend_health()
    test_results.append(("Backend Health", result))
    if not result:
        print_error("Backend is not running. Please start it first.")
        return False
    
    # Test 2: User Registration
    user_data = test_user_registration()
    test_results.append(("User Registration", user_data is not None))
    
    # Test 3: User Login
    token = test_user_login(user_data)
    test_results.append(("User Login", token is not None))
    
    # Test 4: Emergency Alert Creation
    alert_id = test_emergency_alert_creation()
    test_results.append(("Emergency Alert Creation", alert_id is not None))
    
    # Test 5: Guard Response
    guard_response_result = test_guard_response(alert_id, token)
    test_results.append(("Guard Response", guard_response_result))
    
    # Test 6: Alerts Retrieval
    alerts_result = test_alerts_retrieval()
    test_results.append(("Alerts Retrieval", alerts_result))
    
    # Test 7: ESP32 Simulation
    esp32_result = test_esp32_simulation()
    test_results.append(("ESP32 Simulation", esp32_result))
    
    # Summary
    print_header("Test Results Summary")
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\nOverall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("🎉 All tests passed! System is working correctly.")
        print_info("\nNext steps:")
        print_info("1. Test mobile app connection")
        print_info("2. Configure and test ESP32 hardware")
        print_info("3. Test web dashboard")
        return True
    else:
        print_error(f"❌ {total - passed} tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    try:
        success = run_complete_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_info("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)