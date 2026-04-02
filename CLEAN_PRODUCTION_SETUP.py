#!/usr/bin/env python3
"""
CLEAN PRODUCTION SETUP - Remove all test data and restart with real data only
This script:
1. Deletes the old database to remove all test/fake data
2. Creates a fresh database
3. Only creates admin user - NO sample devices
4. All devices will be created from real ESP32 data
"""

import os
import sys
import shutil
from pathlib import Path

def main():
    print("=" * 80)
    print("🔧 CLEAN PRODUCTION SETUP - Real Data Only")
    print("=" * 80)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent / "backend_anti"
    os.chdir(backend_dir)
    
    # Add backend dir to Python path
    sys.path.insert(0, str(backend_dir))
    
    # Step 1: Delete old database file
    db_file = Path("anti_drowning.db")
    if db_file.exists():
        print(f"\n🗑️  Deleting old database: {db_file}")
        db_file.unlink()
        print("✅ Old database deleted")
    else:
        print(f"\n⏭️  No old database found")
    
    # Step 2: Delete __pycache__ to ensure fresh imports
    print("\n🧹 Cleaning cache files...")
    for pycache in Path(".").rglob("__pycache__"):
        shutil.rmtree(pycache)
    print("✅ Cache cleaned")
    
    # Step 3: Initialize fresh database
    print("\n📊 Initializing fresh database...")
    print("   - Importing database module...")
    
    try:
        from database import init_database
        init_database()
        print("✅ Fresh database initialized")
        print("   - Admin user created (phone: admin, password: admin123)")
        print("   - NO sample devices created")
        print("   - Devices will be auto-created from real ESP32 data")
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize database: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print("✅ SETUP COMPLETE - System ready for real ESP32 data only!")
    print("=" * 80)
    print("\n📋 Next Steps:")
    print("1. Power on your ESP32 devices")
    print("2. Ensure ESP32 has WiFi credentials configured")
    print("3. Start the backend: python main.py")
    print("4. ESP32 data will now be saved directly to database")
    print("5. Check your Flutter app for real alerts")
    print("\n🚨 Only REAL data from ESP32 will be saved!")
    print("🚫 No test data will be created")
    print("=" * 80)

if __name__ == "__main__":
    main()
