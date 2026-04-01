#!/usr/bin/env python3
"""
Force clear all alerts via API and create single test case
"""
import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def get_all_alerts():
    """Get all current alerts"""
    try:
        response = requests.get(f"{API_BASE}/alerts", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get('alerts', [])
        else:
            print(f"❌ Failed to get alerts: HTTP {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting alerts: {e}")
        return []

def clear_all_alerts_via_backend():
    """Clear all alerts by adding a delete endpoint or manual method"""
    print("🗑️  Force Clearing All Alerts")
    print("=" * 40)
    
    alerts = get_all_alerts()
    print(f"📊 Found {len(alerts)} alerts to clear")
    
    if len(alerts) == 0:
        print("✅ No alerts to clear")
        return True
    
    # Since there's no delete endpoint, let's create one temporarily
    # or use a workaround
    print("⚠️  No direct delete API available")
    print("💡 Creating workaround...")
    
    return False

def create_delete_endpoint_request():
    """Request to add a delete endpoint to the backend"""
    print("\n🔧 Backend Modification Needed")
    print("=" * 35)
    print("To clear the database, we need to add a delete endpoint.")
    print("I'll create the code for you to add to the backend.")
    
    delete_endpoint_code = '''
# Add this to backend_anti/routes/alerts.py

@router.delete("/alerts/clear-all", response_model=SuccessResponse)
async def clear_all_alerts(db: Session = Depends(get_db)):
    """
    Clear all alerts from the database (for testing purposes)
    """
    try:
        # Delete all alerts
        deleted_count = db.query(Alert).count()
        db.query(Alert).delete()
        db.commit()
        
        return SuccessResponse(
            message=f"All alerts cleared successfully. Deleted {deleted_count} alerts."
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear alerts: {str(e)}"
        )
'''
    
    print("📝 Code to add to backend:")
    print(delete_endpoint_code)
    
    return delete_endpoint_code

def try_clear_via_new_endpoint():
    """Try to clear using the new endpoint if it exists"""
    print("\n🧪 Trying New Clear Endpoint")
    print("-" * 30)
    
    try:
        response = requests.delete(f"{API_BASE}/alerts/clear-all", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ {result.get('message', 'Alerts cleared')}")
            return True
        elif response.status_code == 404:
            print("⚠️  Clear endpoint not available yet")
            return False
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_single_test_case():
    """Create one test case"""
    print("\n🚨 Creating Single Test Case")
    print("=" * 35)
    
    test_case = {
        "device_id": "JALGAON_04_JALGAON_HOSPITAL",
        "danger": True,
        "latitude": 20.95,
        "longitude": 75.556
    }
    
    print(f"📍 Device: {test_case['device_id']}")
    print(f"🚨 Status: EMERGENCY")
    print(f"📍 Location: {test_case['latitude']}, {test_case['longitude']}")
    
    try:
        response = requests.post(
            f"{API_BASE}/alert",
            headers={"Content-Type": "application/json"},
            json=test_case,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            alert_id = result.get('alert_id', 'Unknown')
            print(f"✅ Emergency created! Alert ID: {alert_id}")
            return alert_id
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    """Main function"""
    print("🧹 Force Clear Database via API")
    print("=" * 50)
    print(f"🌐 Backend: {BASE_URL}")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check current alerts
    alerts = get_all_alerts()
    print(f"📊 Current alerts in system: {len(alerts)}")
    
    if len(alerts) > 0:
        print("🗑️  Need to clear existing alerts...")
        
        # Try the new clear endpoint
        if try_clear_via_new_endpoint():
            print("✅ Alerts cleared via API!")
        else:
            print("\n" + "=" * 50)
            print("⚠️  MANUAL BACKEND UPDATE NEEDED")
            print("=" * 50)
            
            # Show the code to add
            create_delete_endpoint_request()
            
            print("\n📋 Steps to fix:")
            print("1. Stop your backend server")
            print("2. Add the delete endpoint code above to backend_anti/routes/alerts.py")
            print("3. Restart your backend server")
            print("4. Run this script again")
            print("\nOr alternatively:")
            print("1. Access your database directly (Supabase dashboard)")
            print("2. Run: DELETE FROM alerts;")
            print("3. Run this script again")
            
            return
    
    # Create single test case
    alert_id = create_single_test_case()
    
    if alert_id:
        # Verify
        time.sleep(1)
        final_alerts = get_all_alerts()
        
        print(f"\n📊 Final check: {len(final_alerts)} alerts in system")
        
        if len(final_alerts) == 1:
            print("🎉 Perfect! Only 1 test case exists")
            print("\n💡 Now test:")
            print("   📱 Mobile app - emergency notification")
            print("   🌐 Website - single case with guard responses")
            print("   🗺️  Google Maps integration")
        else:
            print(f"⚠️  Expected 1 alert, found {len(final_alerts)}")
    
    print("\n" + "=" * 50)
    print("✅ Script completed!")

if __name__ == "__main__":
    main()