#!/usr/bin/env python3
"""
Create and test a single emergency case
"""
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def create_single_emergency():
    """Create one emergency case"""
    print("🚨 Creating Single Emergency Case")
    print("=" * 40)
    
    # Single test case
    emergency_data = {
        "device_id": "JALGAON_04_JALGAON_HOSPITAL",
        "danger": True,
        "latitude": 20.95,
        "longitude": 75.556
    }
    
    print(f"📍 Device: {emergency_data['device_id']}")
    print(f"🚨 Status: EMERGENCY")
    print(f"📍 Location: {emergency_data['latitude']}, {emergency_data['longitude']}")
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    try:
        response = requests.post(
            f"{API_BASE}/alert",
            headers={"Content-Type": "application/json"},
            json=emergency_data,
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
    """Add some guard responses"""
    print(f"\n👮 Adding Guard Responses")
    print("-" * 30)
    
    responses = [
        {
            "case_id": f"CASE{str(alert_id).zfill(3)}",
            "action": "accepted",
            "action_by": "Dr. Rajesh Kumar"
        },
        {
            "case_id": f"CASE{str(alert_id).zfill(3)}",
            "action": "completed",
            "action_by": "Lifeguard Priya"
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

def verify_single_case():
    """Verify the case was created"""
    print(f"\n📊 Verifying Case")
    print("-" * 20)
    
    try:
        response = requests.get(f"{API_BASE}/alerts", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            print(f"Total cases: {len(alerts)}")
            
            if len(alerts) >= 1:
                alert = alerts[0]  # Get the latest
                print(f"✅ Latest case:")
                print(f"   ID: {alert['id']}")
                print(f"   Device: {alert['device_id']}")
                print(f"   Status: {'🚨 DANGER' if alert['danger'] else '✅ SAFE'}")
                print(f"   Location: {alert['latitude']}, {alert['longitude']}")
                return True
            else:
                print("❌ No cases found")
                return False
                
        else:
            print(f"❌ API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Single Emergency Case Test")
    print("=" * 40)
    print(f"🌐 Backend: {BASE_URL}")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Create emergency
    alert_id = create_single_emergency()
    
    if alert_id:
        # Wait a moment
        time.sleep(1)
        
        # Add guard responses
        add_guard_responses(alert_id)
        
        # Wait a moment
        time.sleep(1)
        
        # Verify
        if verify_single_case():
            print("\n" + "=" * 40)
            print("🎉 Single Case Test Complete!")
            print("\n💡 Now test:")
            print("   📱 Mobile app - should show notification")
            print("   🌐 Website - should show 1 case with guard responses")
            print("   🗺️  Maps - click 'View Maps' to see location")
            print("   👁️  Details - click 'View Details' for full info")
            print(f"\n🔗 Direct link: https://www.google.com/maps?q=20.95,75.556")
        else:
            print("\n❌ Verification failed")
    else:
        print("\n❌ Failed to create emergency case")

if __name__ == "__main__":
    main()