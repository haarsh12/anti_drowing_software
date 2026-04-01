#!/usr/bin/env python3
"""
Test script for guard response functionality
"""
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def test_guard_response():
    """Test the guard response endpoint"""
    print("🧪 Testing Guard Response System")
    print("=" * 50)
    
    # Test data
    test_responses = [
        {
            "case_id": "CASE001",
            "action": "accepted",
            "action_by": "Rajesh Kumar"
        },
        {
            "case_id": "CASE001", 
            "action": "completed",
            "action_by": "Priya Sharma"
        },
        {
            "case_id": "CASE002",
            "action": "not_available", 
            "action_by": "Amit Patel"
        }
    ]
    
    print("📤 Sending guard responses...")
    
    for i, response_data in enumerate(test_responses, 1):
        try:
            print(f"\n{i}. Testing response: {response_data['action']} by {response_data['action_by']}")
            
            response = requests.post(
                f"{API_BASE}/guard-response",
                headers={"Content-Type": "application/json"},
                json=response_data,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                result = response.json()
                print(f"   ✅ Success: {result.get('message', 'Response recorded')}")
            else:
                print(f"   ❌ Failed: HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Network error: {e}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Guard response testing completed!")

def test_alerts_with_responses():
    """Test fetching alerts to see if they include guard responses"""
    print("\n🔍 Testing Alerts API")
    print("=" * 50)
    
    try:
        response = requests.get(f"{API_BASE}/alerts", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            print(f"📊 Found {len(alerts)} alerts")
            
            for alert in alerts[:3]:  # Show first 3 alerts
                print(f"\n📋 Alert ID: {alert['id']}")
                print(f"   Device: {alert['device_id']}")
                print(f"   Status: {'🚨 DANGER' if alert['danger'] else '✅ SAFE'}")
                print(f"   Location: {alert['latitude']:.4f}, {alert['longitude']:.4f}")
                print(f"   Time: {alert['timestamp']}")
                
                # Check for guard responses (if implemented)
                if 'guard_responses' in alert:
                    responses = alert['guard_responses']
                    print(f"   Guard Responses: {len(responses)}")
                    for resp in responses:
                        print(f"     - {resp['action_by']}: {resp['action']}")
                else:
                    print("   Guard Responses: Not yet implemented in backend")
        else:
            print(f"❌ Failed to fetch alerts: HTTP {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main test function"""
    print("🚨 Emergency System - Guard Response Testing")
    print("=" * 60)
    print(f"🌐 Testing against: {BASE_URL}")
    print(f"⏰ Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test guard responses
    test_guard_response()
    
    # Test alerts API
    test_alerts_with_responses()
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print("\n💡 Next steps:")
    print("   1. Check backend logs for guard response records")
    print("   2. Test mobile app emergency responses")
    print("   3. Verify website shows guard response data")
    print("   4. Test system notifications on mobile device")

if __name__ == "__main__":
    main()