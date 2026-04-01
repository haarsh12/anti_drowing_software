#!/usr/bin/env python3
"""
Manual database cleanup for different database systems
"""
import os
import sqlite3
import sys
from datetime import datetime

def cleanup_sqlite():
    """Clean up SQLite database"""
    print("🗃️  SQLite Database Cleanup")
    print("=" * 30)
    
    # Possible SQLite database locations
    db_files = [
        "backend_anti/alerts.db",
        "alerts.db",
        "backend_anti/database.db", 
        "database.db",
        "backend_anti/app.db",
        "app.db"
    ]
    
    found_db = False
    
    for db_file in db_files:
        if os.path.exists(db_file):
            found_db = True
            print(f"📁 Found database: {db_file}")
            
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()
                
                # Get table info
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                print(f"   Tables: {[table[0] for table in tables]}")
                
                # Clear alerts table if it exists
                if any('alerts' in table[0].lower() for table in tables):
                    cursor.execute("DELETE FROM alerts")
                    cursor.execute("DELETE FROM sqlite_sequence WHERE name='alerts'")
                    conn.commit()
                    
                    # Verify
                    cursor.execute("SELECT COUNT(*) FROM alerts")
                    count = cursor.fetchone()[0]
                    
                    print(f"   ✅ Cleared alerts table (remaining: {count})")
                else:
                    print("   ⚠️  No alerts table found")
                
                conn.close()
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
    
    if not found_db:
        print("⚠️  No SQLite database files found")
    
    return found_db

def cleanup_supabase():
    """Instructions for Supabase cleanup"""
    print("\n🌐 Supabase Database Cleanup")
    print("=" * 30)
    print("If using Supabase, you can:")
    print("1. Go to your Supabase dashboard")
    print("2. Open SQL Editor")
    print("3. Run: DELETE FROM alerts;")
    print("4. Run: ALTER SEQUENCE alerts_id_seq RESTART WITH 1;")

def delete_database_files():
    """Delete database files completely"""
    print("\n🗑️  Delete Database Files")
    print("=" * 25)
    
    db_files = [
        "backend_anti/alerts.db",
        "alerts.db", 
        "backend_anti/database.db",
        "database.db",
        "backend_anti/app.db",
        "app.db"
    ]
    
    deleted = False
    
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"✅ Deleted: {db_file}")
                deleted = True
            except Exception as e:
                print(f"❌ Failed to delete {db_file}: {e}")
    
    if deleted:
        print("✅ Database files deleted - will be recreated fresh")
    else:
        print("⚠️  No database files found to delete")

def main():
    """Main cleanup function"""
    print("🧹 Manual Database Cleanup")
    print("=" * 40)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("Choose cleanup method:")
    print("1. Clear SQLite database content (recommended)")
    print("2. Delete database files completely")
    print("3. Show Supabase cleanup instructions")
    print("4. Do all SQLite cleanup methods")
    print()
    
    try:
        choice = input("Enter choice (1-4): ").strip()
        print()
        
        if choice == "1":
            cleanup_sqlite()
        elif choice == "2":
            delete_database_files()
        elif choice == "3":
            cleanup_supabase()
        elif choice == "4":
            cleanup_sqlite()
            delete_database_files()
        else:
            print("❌ Invalid choice")
            return
        
        print("\n" + "=" * 40)
        print("✅ Cleanup completed!")
        print("\n💡 Next steps:")
        print("   1. Restart your backend server")
        print("   2. Run: python test_single_case.py")
        print("   3. Check mobile app and website")
        
    except KeyboardInterrupt:
        print("\n\n❌ Cleanup cancelled")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()