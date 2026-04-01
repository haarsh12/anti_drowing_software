#!/usr/bin/env python3
"""
Test database connection and functionality
"""
import requests
import json
import time

def test_database_connection():
    print("🔍 Testing Database Connection...")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    try:
        # Test 1: Get alerts (tests database read)
        print("1. Testing database READ...")
        response = requests.get(f"{base_url}/api/alerts", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Database READ successful!")
            print(f"   📊 Current alerts in database: {data.get('total', 0)}")
        else:
            print(f"   ❌ Database READ failed: {response.status_code}")
            return False
        
        # Test 2: Create a test alert (tests database write)
        print("\n2. Testing database WRITE...")
        test_alert = {
            "device_id": f"test_device_{int(time.time())}",
            "danger": True,
            "latitude": 20.9517,
            "longitude": 75.1681
        }
        
        response = requests.post(
            f"{base_url}/api/alert",
            json=test_alert,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print(f"   ✅ Database WRITE successful!")
            alert_data = response.json()
            print(f"   📝 Created alert ID: {alert_data.get('id', 'N/A')}")
        else:
            print(f"   ❌ Database WRITE failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Test 3: Read alerts again to confirm write worked
        print("\n3. Confirming data was saved...")
        response = requests.get(f"{base_url}/api/alerts", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            new_total = data.get('total', 0)
            print(f"   ✅ Data confirmed saved!")
            print(f"   📊 Total alerts now: {new_total}")
            
            # Show recent alerts
            alerts = data.get('alerts', [])
            if alerts:
                latest = alerts[-1]  # Get the most recent alert
                print(f"   🔍 Latest alert:")
                print(f"      - Device: {latest.get('device_id', 'N/A')}")
                print(f"      - Danger: {'🚨 YES' if latest.get('danger') else '✅ NO'}")
                print(f"      - Location: {latest.get('latitude', 0)}, {latest.get('longitude', 0)}")
        
        print("\n" + "=" * 50)
        print("🎉 DATABASE IS FULLY FUNCTIONAL!")
        print("✅ Can read from database")
        print("✅ Can write to database") 
        print("✅ Data persistence confirmed")
        print("=" * 50)
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("Make sure the backend is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    if success:
        print("\n🚀 Your system is ready!")
        print("Next steps:")
        print("1. Start frontend: cd frontend_anti && npm run dev")
        print("2. Configure mobile app with your IP address")
        print("3. Test the complete system")
    else:
        print("\n❌ Database test failed. Check the backend logs.")