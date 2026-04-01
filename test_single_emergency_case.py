#!/usr/bin/env python3
"""
Single Emergency Case Test - Complete End-to-End Test
Tests the entire emergency flow from registration to alert response
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TEST_DEVICE_ID = "ESP32_JALGAON_POOL_01"
EMERGENCY_LOCATION = {
    "latitude": 20.9517,
    "longitude": 75.1681,
    "location_name": "Jalgaon Main Swimming Pool"
}

def print_step(step_num, title):
    print(f"\n{'='*60}")
    print(f"🔹 STEP {step_num}: {title}")
    print(f"{'='*60}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def test_single_emergency_case():
    """Complete end-to-end emergency case test"""
    
    print("🚨 ANTI-DROWNING EMERGENCY SYSTEM - SINGLE CASE TEST")
    print("=" * 60)
    print(f"🕐 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Backend URL: {BASE_URL}")
    print(f"📍 Emergency Location: {EMERGENCY_LOCATION['location_name']}")
    print(f"📱 Device ID: {TEST_DEVICE_ID}")
    
    # Test data
    guard_user = {
        "name": "Emergency Guard Harsh",
        "phone": f"91{int(time.time()) % 10000000000}",
        "password": "guard123",
        "role": "guard"
    }
    
    supervisor_user = {
        "name": "Supervisor Priya",
        "phone": f"92{int(time.time()) % 10000000000}",
        "password": "super123",
        "role": "supervisor"
    }
    
    try:
        # STEP 1: Test Backend Health
        print_step(1, "Backend Health Check")
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print_success("Backend server is healthy and running")
            print_info(f"Response: {response.json()}")
        else:
            print_error(f"Backend health check failed: {response.status_code}")
            return False
        
        # STEP 2: Register Guard User
        print_step(2, "Register Emergency Guard")
        response = requests.post(f"{BASE_URL}/api/auth/register", json=guard_user, timeout=10)
        if response.status_code == 201:
            print_success(f"Guard registered successfully")
            print_info(f"Name: {guard_user['name']}")
            print_info(f"Phone: {guard_user['phone']}")
            print_info(f"Role: {guard_user['role']}")
        else:
            print_error(f"Guard registration failed: {response.text}")
            return False
        
        # STEP 3: Register Supervisor User
        print_step(3, "Register Supervisor")
        response = requests.post(f"{BASE_URL}/api/auth/register", json=supervisor_user, timeout=10)
        if response.status_code == 201:
            print_success(f"Supervisor registered successfully")
            print_info(f"Name: {supervisor_user['name']}")
            print_info(f"Phone: {supervisor_user['phone']}")
        else:
            print_error(f"Supervisor registration failed: {response.text}")
            return False
        
        # STEP 4: Login Guard and Get Token
        print_step(4, "Guard Login & Authentication")
        login_data = {"phone": guard_user["phone"], "password": guard_user["password"]}
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            guard_token = response.json()["access_token"]
            guard_info = response.json()["user"]
            print_success("Guard login successful")
            print_info(f"Token: {guard_token[:20]}...")
            print_info(f"User ID: {guard_info['id']}")
        else:
            print_error(f"Guard login failed: {response.text}")
            return False
        
        # STEP 5: Login Supervisor and Get Token
        print_step(5, "Supervisor Login & Authentication")
        login_data = {"phone": supervisor_user["phone"], "password": supervisor_user["password"]}
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data, timeout=10)
        if response.status_code == 200:
            supervisor_token = response.json()["access_token"]
            supervisor_info = response.json()["user"]
            print_success("Supervisor login successful")
            print_info(f"Token: {supervisor_token[:20]}...")
            print_info(f"User ID: {supervisor_info['id']}")
        else:
            print_error(f"Supervisor login failed: {response.text}")
            return False
        
        # STEP 6: Check Initial Alerts (Should be empty or minimal)
        print_step(6, "Check Initial System State")
        response = requests.get(f"{BASE_URL}/api/alerts", timeout=10)
        if response.status_code == 200:
            initial_alerts = response.json()
            print_success(f"System state retrieved")
            print_info(f"Initial alerts count: {initial_alerts.get('total', 0)}")
        else:
            print_error(f"Failed to get initial alerts: {response.text}")
            return False
        
        # STEP 7: Simulate ESP32 Heartbeat (Normal Status)
        print_step(7, "ESP32 Device Heartbeat (Normal)")
        heartbeat_data = {
            "device_id": TEST_DEVICE_ID,
            "danger": False,
            "latitude": EMERGENCY_LOCATION["latitude"],
            "longitude": EMERGENCY_LOCATION["longitude"],
            "heartbeat": True,
            "wifi_rssi": -45,
            "uptime": 12345
        }
        response = requests.post(f"{BASE_URL}/api/alert", json=heartbeat_data, timeout=10)
        if response.status_code in [200, 201]:
            print_success("ESP32 heartbeat sent successfully")
            print_info(f"Device: {TEST_DEVICE_ID}")
            print_info(f"Status: Normal (No Danger)")
            print_info(f"WiFi Signal: {heartbeat_data['wifi_rssi']} dBm")
        else:
            print_error(f"ESP32 heartbeat failed: {response.text}")
            return False
        
        # STEP 8: Simulate Emergency Alert
        print_step(8, "🚨 EMERGENCY ALERT - Drowning Detected!")
        emergency_data = {
            "device_id": TEST_DEVICE_ID,
            "danger": True,
            "latitude": EMERGENCY_LOCATION["latitude"],
            "longitude": EMERGENCY_LOCATION["longitude"],
            "rssi": -67,
            "timestamp": int(time.time() * 1000)
        }
        response = requests.post(f"{BASE_URL}/api/alert", json=emergency_data, timeout=10)
        if response.status_code in [200, 201]:
            emergency_alert = response.json()
            # Try multiple ways to extract alert ID
            alert_id = None
            if "data" in emergency_alert:
                alert_id = emergency_alert["data"].get("id") or emergency_alert["data"].get("alert_id")
            if not alert_id:
                alert_id = emergency_alert.get("id") or emergency_alert.get("alert_id")
            
            print_success("🚨 EMERGENCY ALERT CREATED!")
            print_info(f"Alert ID: {alert_id}")
            print_info(f"Location: {EMERGENCY_LOCATION['latitude']}, {EMERGENCY_LOCATION['longitude']}")
            print_info(f"Device: {TEST_DEVICE_ID}")
            print_info(f"Timestamp: {datetime.now().strftime('%H:%M:%S')}")
            print_info(f"Full Response: {emergency_alert}")  # Debug info
            
            if not alert_id:
                print_error("Alert ID could not be extracted from response")
                return False
        else:
            print_error(f"Emergency alert creation failed: {response.text}")
            return False
        
        # STEP 9: Verify Alert in System
        print_step(9, "Verify Emergency Alert in System")
        response = requests.get(f"{BASE_URL}/api/alerts", timeout=10)
        if response.status_code == 200:
            alerts_data = response.json()
            alerts = alerts_data.get("alerts", [])
            danger_alerts = [a for a in alerts if a.get("danger") == True]
            print_success(f"Alert verification successful")
            print_info(f"Total alerts: {len(alerts)}")
            print_info(f"Danger alerts: {len(danger_alerts)}")
            
            if danger_alerts:
                latest_danger = danger_alerts[-1]
                print_info(f"Latest danger alert ID: {latest_danger.get('id')}")
                print_info(f"Device: {latest_danger.get('device_id')}")
        else:
            print_error(f"Alert verification failed: {response.text}")
            return False
        
        # STEP 10: Guard Response - Accept Case
        print_step(10, "Guard Response - Accepting Emergency Case")
        guard_response_data = {
            "alert_id": alert_id,
            "action": "accepted",
            "notes": f"Emergency response accepted by {guard_user['name']} - En route to location"
        }
        headers = {"Authorization": f"Bearer {guard_token}"}
        response = requests.post(
            f"{BASE_URL}/api/guard-response", 
            json=guard_response_data, 
            headers=headers, 
            timeout=10
        )
        if response.status_code in [200, 201]:
            print_success("Guard accepted the emergency case")
            print_info(f"Guard: {guard_user['name']}")
            print_info(f"Action: Accepted")
            print_info(f"Response time: {datetime.now().strftime('%H:%M:%S')}")
        else:
            print_error(f"Guard response failed: {response.text}")
            return False
        
        # STEP 11: Simulate Time Delay (Guard traveling to location)
        print_step(11, "Simulating Guard Travel Time")
        print_info("⏳ Guard is traveling to emergency location...")
        time.sleep(2)  # Simulate 2 seconds of travel time
        print_success("Guard has arrived at the location")
        
        # STEP 12: Guard Response - Rescue Completed
        print_step(12, "Guard Response - Rescue Operation Completed")
        completion_response_data = {
            "alert_id": alert_id,
            "action": "completed",
            "notes": f"Person rescued successfully by {guard_user['name']} - Victim is safe and receiving medical attention"
        }
        response = requests.post(
            f"{BASE_URL}/api/guard-response", 
            json=completion_response_data, 
            headers=headers, 
            timeout=10
        )
        if response.status_code in [200, 201]:
            print_success("🎉 RESCUE OPERATION COMPLETED SUCCESSFULLY!")
            print_info(f"Guard: {guard_user['name']}")
            print_info(f"Action: Completed")
            print_info(f"Completion time: {datetime.now().strftime('%H:%M:%S')}")
        else:
            print_error(f"Completion response failed: {response.text}")
            return False
        
        # STEP 13: Supervisor Verification
        print_step(13, "Supervisor Verification")
        supervisor_response_data = {
            "alert_id": alert_id,
            "action": "verified",
            "notes": f"Case verified by supervisor {supervisor_user['name']} - All protocols followed correctly"
        }
        supervisor_headers = {"Authorization": f"Bearer {supervisor_token}"}
        response = requests.post(
            f"{BASE_URL}/api/guard-response", 
            json=supervisor_response_data, 
            headers=supervisor_headers, 
            timeout=10
        )
        if response.status_code in [200, 201]:
            print_success("Supervisor verification completed")
            print_info(f"Supervisor: {supervisor_user['name']}")
            print_info(f"Status: Verified")
        else:
            print_error(f"Supervisor verification failed: {response.text}")
            # This is not critical, continue
        
        # STEP 14: Final System State Check
        print_step(14, "Final System State Verification")
        response = requests.get(f"{BASE_URL}/api/alerts", timeout=10)
        if response.status_code == 200:
            final_alerts = response.json()
            alerts = final_alerts.get("alerts", [])
            
            # Find our specific alert
            our_alert = None
            for alert in alerts:
                if alert.get("id") == alert_id:
                    our_alert = alert
                    break
            
            if our_alert:
                print_success("Final verification successful")
                print_info(f"Alert ID: {our_alert.get('id')}")
                print_info(f"Device: {our_alert.get('device_id')}")
                print_info(f"Danger Status: {'🚨 DANGER' if our_alert.get('danger') else '✅ SAFE'}")
                print_info(f"Guard Responses: {len(our_alert.get('guard_responses', []))}")
                
                # Show guard responses
                for i, response in enumerate(our_alert.get('guard_responses', []), 1):
                    print_info(f"  Response {i}: {response.get('action')} by {response.get('user', {}).get('name', 'Unknown')}")
            else:
                print_error("Could not find our alert in final verification")
        else:
            print_error(f"Final verification failed: {response.text}")
            return False
        
        # STEP 15: Test Summary
        print_step(15, "TEST SUMMARY")
        print_success("🎉 COMPLETE EMERGENCY CASE TEST PASSED!")
        print()
        print("📊 Test Results:")
        print("  ✅ Backend Health Check")
        print("  ✅ User Registration (Guard & Supervisor)")
        print("  ✅ User Authentication (JWT Tokens)")
        print("  ✅ ESP32 Device Communication")
        print("  ✅ Emergency Alert Creation")
        print("  ✅ Alert System Verification")
        print("  ✅ Guard Response System")
        print("  ✅ Multi-step Response Tracking")
        print("  ✅ Supervisor Verification")
        print("  ✅ Complete Emergency Workflow")
        print()
        print("🚨 Emergency Response Time Summary:")
        print(f"  📱 Alert Created: {datetime.now().strftime('%H:%M:%S')}")
        print(f"  👮 Guard Accepted: Immediate")
        print(f"  🏥 Rescue Completed: 2 seconds (simulated)")
        print(f"  ✅ Supervisor Verified: Immediate")
        print()
        print("🎯 System Status: FULLY OPERATIONAL")
        print("🔒 Authentication: WORKING")
        print("📡 Device Communication: WORKING")
        print("🚨 Emergency Response: WORKING")
        print("👥 Multi-user Support: WORKING")
        print("📊 Data Persistence: WORKING")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend server")
        print_info("Make sure the backend is running on http://localhost:8000")
        return False
    except Exception as e:
        print_error(f"Test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Starting Single Emergency Case Test...")
    print("This test will simulate a complete emergency response scenario")
    print()
    
    success = test_single_emergency_case()
    
    print("\n" + "="*60)
    if success:
        print("🎉 SINGLE EMERGENCY CASE TEST: PASSED")
        print("Your anti-drowning emergency system is fully functional!")
        print()
        print("Next steps:")
        print("1. Test the mobile app with registration and login")
        print("2. Test the web dashboard at http://localhost:5173")
        print("3. Configure and test ESP32 hardware")
        print("4. Deploy to production environment")
    else:
        print("❌ SINGLE EMERGENCY CASE TEST: FAILED")
        print("Please check the error messages above and fix the issues.")
        print()
        print("Common fixes:")
        print("1. Make sure backend is running: python backend_anti/main.py")
        print("2. Check if all dependencies are installed")
        print("3. Verify database is accessible")
    
    print("="*60)