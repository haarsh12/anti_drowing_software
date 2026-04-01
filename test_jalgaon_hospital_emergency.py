#!/usr/bin/env python3
"""
Test script for Jalgaon Hospital emergency alert
Based on the device data shown in the error message
"""
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_jalgaon_hospital_emergency():
    """Test emergency alert for Jalgaon Hospital device"""
    print("🏥 Testing Jalgaon Hospital Emergency Alert")
    print("=" * 60)
    
    # Exact data from your error message
    emergency_data = {
        "device_id": "JALGAON_04_JALGAON_HOSPITAL",
        "danger": True,
        "latitude": 20.95,
        "longitude": 75.556
    }
    
    print(f"📍 Device: {emergency_data['device_id']}")
    print(f"🚨 Danger Status: {emergency_data['danger']}")
    print(f"📍 Location: {emergency_data['latitude']}, {emergency_data['longitude']}")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        print("📤 Sending emergency alert to backend...")
        
        response = requests.post(
            f"{API_BASE}/alert",
            headers={"Content-Type": "application/json"},
            json=emergency_data,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            alert_id = result.get('alert_id', 'Unknown')
            print(f"✅ Emergency alert created successfully!")
            print(f"   Alert ID: {alert_id}")
            print(f"   Message: {result.get('message', 'Alert created')}")
            
            # Test guard response for this alert
            test_guard_response_for_alert(alert_id)
            
        else:
            print(f"❌ Failed to create alert: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_guard_response_for_alert(alert_id):
    """Test guard responses for the created alert"""
    print(f"\n👮 Testing Guard Responses for Alert {alert_id}")
    print("-" * 40)
    
    # Simulate guard responses
    guard_responses = [
        {
            "case_id": f"CASE{str(alert_id).zfill(3)}",
            "action": "accepted",
            "action_by": "Dr. Rajesh Kumar - Jalgaon Hospital"
        },
        {
            "case_id": f"CASE{str(alert_id).zfill(3)}",
            "action": "completed", 
            "action_by": "Lifeguard Priya Sharma"
        }
    ]
    
    for i, response_data in enumerate(guard_responses, 1):
        try:
            print(f"\n{i}. Guard Response: {response_data['action']} by {response_data['action_by']}")
            
            response = requests.post(
                f"{API_BASE}/guard-response",
                headers={"Content-Type": "application/json"},
                json=response_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"   ✅ Response recorded: {result.get('message', 'Success')}")
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Network error: {e}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

def check_alerts_status():
    """Check current alerts in the system"""
    print(f"\n📊 Checking Current Alerts Status")
    print("-" * 40)
    
    try:
        response = requests.get(f"{API_BASE}/alerts", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            print(f"Total alerts in system: {len(alerts)}")
            
            # Show recent Jalgaon Hospital alerts
            jalgaon_alerts = [a for a in alerts if 'JALGAON' in a.get('device_id', '')]
            
            if jalgaon_alerts:
                print(f"\nJalgaon Hospital alerts: {len(jalgaon_alerts)}")
                for alert in jalgaon_alerts[:3]:  # Show last 3
                    status = "🚨 DANGER" if alert['danger'] else "✅ SAFE"
                    print(f"  - ID {alert['id']}: {status} at {alert['timestamp']}")
            else:
                print("No Jalgaon Hospital alerts found")
                
        else:
            print(f"❌ Failed to fetch alerts: HTTP {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main test function"""
    print("🚨 Jalgaon Hospital Emergency System Test")
    print("=" * 60)
    print(f"🌐 Testing against: {BASE_URL}")
    print(f"⏰ Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check current status
    check_alerts_status()
    
    # Test emergency alert
    test_jalgaon_hospital_emergency()
    
    # Wait a moment
    time.sleep(2)
    
    # Check status again
    check_alerts_status()
    
    print("\n" + "=" * 60)
    print("🎉 Jalgaon Hospital emergency test completed!")
    print("\n💡 Next steps:")
    print("   1. Check mobile app for emergency notification")
    print("   2. Verify website dashboard shows the alert")
    print("   3. Test guard response functionality")
    print("   4. Check Google Maps integration with coordinates")
    print(f"   5. Location: https://www.google.com/maps?q=20.95,75.556")

if __name__ == "__main__":
    main()