#!/usr/bin/env python3
"""
Simple script to clear all cases from the database
"""
import requests
import json
import sqlite3
import os
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

# Possible database locations
DB_PATHS = [
    "backend_anti/alerts.db",
    "alerts.db",
    "backend_anti/database.db",
    "database.db"
]

def find_database():
    """Find the database file"""
    for db_path in DB_PATHS:
        if os.path.exists(db_path):
            return db_path
    return None

def clear_database_file():
    """Clear the database file directly"""
    print("🗑️  Clearing Database File")
    print("=" * 30)
    
    db_path = find_database()
    
    if db_path:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Check if alerts table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alerts'")
            if cursor.fetchone():
                # Delete all alerts
                cursor.execute("DELETE FROM alerts")
                conn.commit()
                
                # Reset auto-increment
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='alerts'")
                conn.commit()
                
                print(f"✅ Database cleared: {db_path}")
            else:
                print("⚠️  No alerts table found")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Error clearing database: {e}")
            return False
    else:
        print("⚠️  No database file found")
        return False

def verify_empty_via_api():
    """Check if database is empty via API"""
    print("\n🔍 Verifying via API")
    print("-" * 20)
    
    try:
        response = requests.get(f"{API_BASE}/alerts", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            print(f"📊 Current alerts: {len(alerts)}")
            
            if len(alerts) == 0:
                print("✅ Database is empty")
                return True
            else:
                print("⚠️  Still has alerts:")
                for alert in alerts[:3]:
                    print(f"   - {alert['id']}: {alert['device_id']}")
                return False
                
        else:
            print(f"❌ API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Network error: {e}")
        return False

def main():
    """Main cleanup function"""
    print("🧹 Clear All Cases")
    print("=" * 30)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Method 1: Clear database file
    success = clear_database_file()
    
    # Method 2: Verify via API
    verify_empty_via_api()
    
    print("\n" + "=" * 30)
    if success:
        print("✅ Database cleared successfully!")
        print("\n💡 Next steps:")
        print("   1. Restart backend server")
        print("   2. Run single test case")
        print("   3. Check mobile app and website")
    else:
        print("⚠️  Manual cleanup may be needed")
        print("\n💡 Alternative:")
        print("   1. Stop backend server")
        print("   2. Delete database file manually")
        print("   3. Restart backend server")

if __name__ == "__main__":
    main()