#!/usr/bin/env python3
"""
Quick status check of the system
"""
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

def check_backend():
    """Check if backend is running"""
    print("🔍 Backend Status")
    print("-" * 20)
    
    try:
        response = requests.get(f"{API_BASE}/alerts", timeout=5)
        
        if response.status_code == 200:
            print("✅ Backend is running")
            return True
        else:
            print(f"⚠️  Backend responding with HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return False

def check_alerts():
    """Check current alerts"""
    print("\n📊 Current Alerts")
    print("-" * 20)
    
    try:
        response = requests.get(f"{API_BASE}/alerts", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            print(f"Total alerts: {len(alerts)}")
            
            if len(alerts) == 0:
                print("✅ No alerts (clean database)")
            elif len(alerts) == 1:
                alert = alerts[0]
                print(f"✅ Single alert (perfect for testing):")
                print(f"   ID: {alert['id']}")
                print(f"   Device: {alert['device_id']}")
                print(f"   Status: {'🚨 DANGER' if alert['danger'] else '✅ SAFE'}")
            else:
                print(f"⚠️  Multiple alerts ({len(alerts)}):")
                for alert in alerts[:5]:  # Show first 5
                    status = "🚨 DANGER" if alert['danger'] else "✅ SAFE"
                    print(f"   - {alert['id']}: {alert['device_id']} ({status})")
                if len(alerts) > 5:
                    print(f"   ... and {len(alerts) - 5} more")
            
            return alerts
            
        else:
            print(f"❌ Failed: HTTP {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def check_delete_endpoint():
    """Check if delete endpoint is available"""
    print("\n🗑️  Delete Endpoint Status")
    print("-" * 25)
    
    try:
        # Try to access the delete endpoint (without actually deleting)
        response = requests.options(f"{API_BASE}/alerts/clear-all", timeout=5)
        
        if response.status_code in [200, 405]:  # 405 = Method Not Allowed is OK
            print("✅ Delete endpoint is available")
            return True
        else:
            print(f"⚠️  Delete endpoint status: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Delete endpoint not available: {e}")
        return False

def main():
    """Main status check"""
    print("📋 System Status Check")
    print("=" * 30)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 Backend: {BASE_URL}")
    print()
    
    # Check backend
    backend_ok = check_backend()
    
    if backend_ok:
        # Check alerts
        alerts = check_alerts()
        
        # Check delete endpoint
        delete_ok = check_delete_endpoint()
        
        print("\n" + "=" * 30)
        print("📋 Summary")
        print("-" * 10)
        
        if len(alerts) == 0:
            print("✅ Ready for testing - database is clean")
            print("💡 Run: python test_single_case.py")
        elif len(alerts) == 1:
            print("✅ Perfect for testing - single case exists")
            print("💡 Test mobile app and website now")
        else:
            print(f"⚠️  {len(alerts)} alerts exist - may want to clear")
            if delete_ok:
                print("💡 Run: python clear_and_create_one.py")
            else:
                print("💡 Restart backend first, then run clear script")
        
        if not delete_ok:
            print("⚠️  Delete endpoint not available")
            print("💡 Restart backend to load new endpoint")
    
    else:
        print("\n❌ Backend not running")
        print("💡 Start backend with: python backend_anti/main.py")

if __name__ == "__main__":
    main()