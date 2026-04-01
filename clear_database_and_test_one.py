#!/usr/bin/env python3
"""
Clear all previous cases and test with one clean emergency case
"""
import requests
import json
import time
from datetime import datetime
import sqlite3
import os

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"
DB_PATH = "backend_anti/alerts.db"  # Adjust path if needed

def clear_database():
    """Clear all alerts from the database"""
    print("🗑️  Clearing Database")
    print("=" * 40)
    
    try:
        # Try to connect to SQLite database
        if os.path.exists(DB_PATH):
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Delete all alerts
            cursor.execute("DELETE FROM alerts")
            conn.commit()
            
            # Get count to verify
            cursor.execute("SELECT COUNT(*) FROM alerts")
            count = cursor.fetchone()[0]
            
            conn.close()
            
            print(f"✅ Database cleared successfully!")
            print(f"   Remaining alerts: {count}")
            
        else:
            print("⚠️  Database file not found, will be created fresh")
            
    except Exception as e:
        print(f"❌ Error clearing database: {e}")
        print("   Database will be cleared when backend starts")

def verify_database_empty():
    """Verify database is empty by checking API"""
    print("\n🔍 Verifying Database is Empty")
    print("-" * 40)
    
    try:
        response = requests.get(f"{API_BASE}/alerts", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            print(f"📊 Current alerts in system: {len(alerts)}")
            
            if len(alerts) == 0:
                print("✅ Database is clean and empty")
                return True
            else:
                print("⚠️  Database still has alerts:")
                for alert in alerts[:3]:  # Show first 3
                    print(f"   - Alert {alert['id']}: {alert['device_id']}")
                return False
                
        else:
            print(f"❌ Failed to check database: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False

def create_single_test_case():
    """Create one clean test emergency case"""
    print("\n🚨 Creating Single Test Emergency Case")
    print("=" * 50)
    
    # Single test case - Jalgaon Hospital Emergency
    test_case = {
        "device_id": "JALGAON_04_JALGAON_HOSPITAL",
        "danger": True,
        "latitude": 20.95,
        "longitude": 75.556
    }
    
    print(f"📍 Device: {test_case['device_id']}")
    print(f"🚨 Emergency Status: {test_case['danger']}")
    print(f"📍 Location: {test_case['latitude']}, {test_case['longitude']}")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        print("📤 Creating emergency alert...")
        
        response = requests.post(
            f"{API_BASE}/alert",
            headers={"Content-Type": "application/json"},
            json=test_case,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            alert_id = result.get('alert_id', 'Unknown')
            
            print(f"✅ Emergency alert created successfully!")
            print(f"   Alert ID: {alert_id}")
            print(f"   Case ID: CASE{str(alert_id).zfill(3)}")
            print(f"   Message: {result.get('message', 'Alert created')}")
            
            return alert_id
            
        else:
            print(f"❌ Failed to create alert: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return None

def test_guard_responses(alert_id):
    """Test guard responses for the single alert"""
    print(f"\n👮 Testing Guard Responses for Alert {alert_id}")
    print("-" * 50)
    
    # Test guard responses
    guard_responses = [
        {
            "case_id": f"CASE{str(alert_id).zfill(3)}",
            "action": "accepted",
            "action_by": "Dr. Rajesh Kumar - Emergency Response Team"
        },
        {
            "case_id": f"CASE{str(alert_id).zfill(3)}",
            "action": "completed",
            "action_by": "Lifeguard Priya Sharma - Jalgaon Hospital"
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
        
        # Wait between responses
        time.sleep(1)

def verify_single_case():
    """Verify only one case exists in the system"""
    print(f"\n📊 Verifying Single Case in System")
    print("-" * 40)
    
    try:
        response = requests.get(f"{API_BASE}/alerts", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            print(f"Total alerts in system: {len(alerts)}")
            
            if len(alerts) == 1:
                alert = alerts[0]
                print(f"✅ Perfect! Only one case exists:")
                print(f"   - Alert ID: {alert['id']}")
                print(f"   - Case ID: CASE{str(alert['id']).zfill(3)}")
                print(f"   - Device: {alert['device_id']}")
                print(f"   - Status: {'🚨 DANGER' if alert['danger'] else '✅ SAFE'}")
                print(f"   - Location: {alert['latitude']}, {alert['longitude']}")
                print(f"   - Time: {alert['timestamp']}")
                return True
            elif len(alerts) == 0:
                print("❌ No alerts found - something went wrong")
                return False
            else:
                print(f"⚠️  Found {len(alerts)} alerts - expected only 1")
                return False
                
        else:
            print(f"❌ Failed to verify: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return False

def main():
    """Main function to clear database and test single case"""
    print("🧹 Database Cleanup & Single Case Test")
    print("=" * 60)
    print(f"🌐 Testing against: {BASE_URL}")
    print(f"⏰ Test time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Step 1: Clear database
    clear_database()
    
    # Step 2: Wait a moment for database to be ready
    print("\n⏳ Waiting for database to be ready...")
    time.sleep(2)
    
    # Step 3: Verify database is empty
    if not verify_database_empty():
        print("\n⚠️  Database might not be completely empty, but continuing...")
    
    # Step 4: Create single test case
    alert_id = create_single_test_case()
    
    if alert_id:
        # Step 5: Wait a moment
        time.sleep(2)
        
        # Step 6: Test guard responses
        test_guard_responses(alert_id)
        
        # Step 7: Wait a moment
        time.sleep(2)
        
        # Step 8: Verify only one case exists
        verify_single_case()
        
        print("\n" + "=" * 60)
        print("🎉 Single Case Test Setup Complete!")
        print("\n💡 Next steps:")
        print("   1. Open mobile app to see emergency notification")
        print("   2. Open website dashboard to see the single case")
        print("   3. Test 'View Details' and 'View Maps' buttons")
        print("   4. Verify guard responses are displayed")
        print(f"   5. Google Maps: https://www.google.com/maps?q=20.95,75.556")
        print("\n🔗 Quick Links:")
        print("   - Website: http://localhost:3000")
        print("   - Backend API: http://localhost:8000/api/alerts")
        
    else:
        print("\n❌ Failed to create test case")

if __name__ == "__main__":
    main()