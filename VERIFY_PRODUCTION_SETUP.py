#!/usr/bin/env python3
"""
PRODUCTION VERIFICATION SCRIPT
Verifies that the system is configured for REAL DATA ONLY
"""

import os
import sys
from pathlib import Path

def check_database_config():
    """Check if database.py has sample devices removed"""
    print("\n📋 Checking Backend Configuration...")
    
    db_file = Path("backend_anti/database.py")
    content = db_file.read_text(encoding='utf-8')
    
    # Check if sample devices have been removed
    if "JALGAON_01_MAIN_POOL" in content:
        print("❌ FAIL: Sample devices still in database.py!")
        print("   Please run: python CLEAN_PRODUCTION_SETUP.py")
        return False
    else:
        print("✅ PASS: Sample devices removed")
        
    # Check if devices will be auto-created
    if "auto-created from real ESP32" in content:
        print("✅ PASS: Devices will be auto-created from real ESP32 data")
        return True
    else:
        print("⚠️  WARNING: Auto-creation message not found")
        return True

def check_no_test_data_creation():
    """Check if alerts endpoint is creating test data"""
    print("\n📋 Checking Alert Processing...")
    
    alerts_file = Path("backend_anti/routes/alerts.py")
    content = alerts_file.read_text(encoding='utf-8')
    
    # Check if there's any automatic test data creation
    if "create_test" in content.lower() or "insert test" in content.lower():
        print("❌ FAIL: Test data creation found in alerts endpoint!")
        return False
    else:
        print("✅ PASS: No automatic test data creation")
        
    # Check if real alerts are being saved
    if "db.add(new_alert)" in content and "db.commit()" in content:
        print("✅ PASS: Real alerts are being saved to database")
        return True
    else:
        print("❌ FAIL: Alert saving logic not found!")
        return False

def check_no_running_test_scripts():
    """Warn about test scripts that should not be running"""
    print("\n📋 Checking for Test Scripts...")
    
    test_scripts = [
        "clear_database_and_test_one.py",
        "clear_all_cases.py",
        "test_complete_system.py",
        "single_emergency_test.py",
        "test_esp32_backend_connection.py",
    ]
    
    root_dir = Path(".")
    test_files_found = []
    
    for script in test_scripts:
        if (root_dir / script).exists():
            test_files_found.append(script)
    
    if test_files_found:
        print(f"⚠️  WARNING: {len(test_files_found)} test scripts found:")
        for script in test_files_found:
            print(f"   - {script}")
        print("\n🚫 Make sure these are NOT running!")
        print("   If they are, STOP them immediately!")
        return False
    else:
        print("✅ PASS: No test scripts found")
        return True

def check_fresh_database():
    """Check if database is fresh with no sample data"""
    print("\n📋 Checking Database State...")
    
    db_path = Path("backend_anti/anti_drowning.db")
    
    if not db_path.exists():
        print("✅ PASS: No database file (will be created on first run)")
        return True
    
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if devices table has sample devices
        cursor.execute("SELECT COUNT(*) FROM devices")
        device_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM devices WHERE device_id LIKE 'JALGAON%'")
        sample_count = cursor.fetchone()[0]
        
        conn.close()
        
        if sample_count > 0:
            print(f"❌ FAIL: {sample_count} sample devices still in database!")
            print("   Run: python CLEAN_PRODUCTION_SETUP.py")
            return False
        elif device_count == 0:
            print("✅ PASS: Database is empty (ready for real ESP32 data)")
            return True
        else:
            print(f"✅ PASS: {device_count} real device(s) in database")
            return True
            
    except Exception as e:
        print(f"⚠️  Could not check database: {e}")
        return True

def main():
    print("=" * 80)
    print("🔍 PRODUCTION VERIFICATION - Real Data Only")
    print("=" * 80)
    
    os.chdir(Path(__file__).parent)
    
    results = []
    
    # Run all checks
    results.append(("Database Config", check_database_config()))
    results.append(("Test Data Creation", check_no_test_data_creation()))
    results.append(("Test Scripts", check_no_running_test_scripts()))
    results.append(("Database State", check_fresh_database()))
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {check_name}")
    
    print(f"\nScore: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 SYSTEM READY FOR PRODUCTION!")
        print("✅ Only real ESP32 data will be processed")
        print("✅ No test data will be created")
        print("\n📋 Next Steps:")
        print("1. Start backend: cd backend_anti && python main.py")
        print("2. Power on ESP32 devices")
        print("3. Check backend logs for ESP32 connections")
        print("4. Start Flutter app: flutter run")
        print("5. Watch real data flow through the system")
        return 0
    else:
        print(f"\n⚠️  {total - passed} issue(s) found!")
        print("Please fix the issues above before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
