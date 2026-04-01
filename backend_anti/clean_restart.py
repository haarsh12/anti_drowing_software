#!/usr/bin/env python3
"""
Clean restart - Remove old database and start fresh
"""
import os
import sqlite3

def clean_restart():
    print("🧹 Cleaning up old database...")
    
    # Remove old database file if it exists
    db_file = "anti_drowning.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"✅ Removed old database: {db_file}")
    
    # Initialize fresh database
    print("🔄 Creating fresh database...")
    from database import init_database
    init_database()
    
    print("✅ Clean restart completed!")
    print("Your database is now fresh and ready to use.")

if __name__ == "__main__":
    clean_restart()