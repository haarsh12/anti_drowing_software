#!/usr/bin/env python3
"""
Clear all alerts and create one test case using the new API endpoint
"""
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def clear_all_alerts():
    """Clear all alerts using the new delete endpoint"""
    print("🗑️  Clearing All Alerts")
    print("=" * 25)
    
    try:
        response = requests.delete(f"{API_BASE}/alerts/clear-all", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result.get('message', 'Alerts cleared')}")
            return True
        else:
            print(f"❌ Failed to clear: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def verify_empty():
    """Verify database is empty"""
    print("\n🔍 Verifying Database is Empty")
    print("-" * 30)
    
    try:
        response = requests.get(f"{API_BASE}/alerts", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            print(f"📊 Current alerts: {len(alerts)}")
            
            if len(alerts) == 0:
                print("✅ Database is clean!")
                return True
            else:
                print("⚠️  Still has alerts:")
                for alert in alerts[:3]:
                    print(f"   - {alert['id']}: {alert['device_id']}")
                return False
                
        else:
            print(f"❌ Failed to verify: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_test_case():
    """Create single test emergency case"""
    print("\n🚨 Creating Test Emergency")
    print("=" * 30)
    
    test_data = {
        "device_id": "JALGAON_04_JALGAON_HOSPITAL",
        "danger": True,
        "latitude": 20.95,
        "longitude": 75.556
    }
    
    print(f"📍 Device: {test_data['device_id']}")
    print(f"🚨 Status: EMERGENCY")
    print(f"📍 Location: {test_data['latitude']}, {test_data['longitude']}")
    
    try:
        response = requests.post(
            f"{API_BASE}/alert",
            headers={"Content-Type": "application/json"},
            json=test_data,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            alert_id = result.get('alert_id', 'Unknown')
            print(f"✅ Emergency created!")
            print(f"   Alert ID: {alert_id}")
            print(f"   Case ID: CASE{str(alert_id).zfill(3)}")
            return alert_id
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def add_guard_responses(alert_id):
    """Add guard responses to the test case"""
    print(f"\n👮 Adding Guard Responses")
    print("-" * 25)
    
    responses = [
        {
            "case_id": f"CASE{str(alert_id).zfill(3)}",
            "action": "accepted",
            "action_by": "Dr. Rajesh Kumar"
        },
        {
            "case_id": f"CASE{str(alert_id).zfill(3)}",
            "action": "completed",
            "action_by": "Lifeguard Priya Sharma"
        }
    ]
    
    for i, response_data in enumerate(responses, 1):
        try:
            print(f"{i}. {response_data['action']} by {response_data['action_by']}")
            
            response = requests.post(
                f"{API_BASE}/guard-response",
                headers={"Content-Type": "application/json"},
                json=response_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                print(f"   ✅ Recorded")
            else:
                print(f"   ❌ Failed")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(0.5)

def final_verification():
    """Final verification that only one case exists"""
    print(f"\n📊 Final Verification")
    print("-" * 20)
    
    try:
        response = requests.get(f"{API_BASE}/alerts", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            print(f"Total alerts: {len(alerts)}")
            
            if len(alerts) == 1:
                alert = alerts[0]
                print(f"✅ Perfect! Single test case:")
                print(f"   ID: {alert['id']}")
                print(f"   Device: {alert['device_id']}")
                print(f"   Status: {'🚨 DANGER' if alert['danger'] else '✅ SAFE'}")
                print(f"   Location: {alert['latitude']}, {alert['longitude']}")
                return True
            else:
                print(f"⚠️  Expected 1 alert, found {len(alerts)}")
                return False
                
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main execution"""
    print("🧹 Clear All & Create Single Test Case")
    print("=" * 45)
    print(f"🌐 Backend: {BASE_URL}")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Clear all alerts
    if not clear_all_alerts():
        print("\n❌ Failed to clear alerts. Make sure:")
        print("   1. Backend server is running")
        print("   2. Delete endpoint is added to routes/alerts.py")
        return
    
    # Step 2: Verify empty
    time.sleep(1)
    if not verify_empty():
        print("⚠️  Database not completely empty, but continuing...")
    
    # Step 3: Create test case
    alert_id = create_test_case()
    
    if alert_id:
        # Step 4: Add guard responses
        time.sleep(1)
        add_guard_responses(alert_id)
        
        # Step 5: Final verification
        time.sleep(1)
        if final_verification():
            print("\n" + "=" * 45)
            print("🎉 SUCCESS! Single test case ready!")
            print("\n💡 Now test:")
            print("   📱 Mobile app - emergency notification")
            print("   🌐 Website: http://localhost:3000")
            print("   👁️  Click 'View Details' for full info")
            print("   🗺️  Click 'View Maps' for location")
            print(f"   🔗 Direct Maps: https://www.google.com/maps?q=20.95,75.556")
        else:
            print("\n⚠️  Verification failed, but test case should work")
    else:
        print("\n❌ Failed to create test case")
    
    print("\n" + "=" * 45)
    print("✅ Script completed!")

if __name__ == "__main__":
    main()