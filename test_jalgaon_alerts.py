#!/usr/bin/env python3
"""
Jalgaon Emergency Test
=====================
Sends multiple emergency alerts with exact Jalgaon coordinates to test map markers.
"""

import requests
import json
import time
from datetime import datetime

def send_jalgaon_alerts():
    """Send multiple emergency alerts with Jalgaon coordinates"""
    
    print("🚨 JALGAON EMERGENCY TEST")
    print("=" * 40)
    
    # Backend URL
    backend_url = "http://127.0.0.1:8000"
    
    # Exact Jalgaon locations with precise coordinates
    jalgaon_locations = [
        {
            "name": "Jalgaon Railway Station",
            "lat": 20.947409,
            "lng": 75.554987,
            "danger": True
        },
        {
            "name": "Jalgaon Bus Stand", 
            "lat": 20.945000,
            "lng": 75.558000,
            "danger": True
        },
        {
            "name": "Jalgaon City Center",
            "lat": 20.949000,
            "lng": 75.552000,
            "danger": False  # Previous alert (grey marker)
        },
        {
            "name": "Jalgaon Hospital",
            "lat": 20.950000,
            "lng": 75.556000,
            "danger": True
        },
        {
            "name": "Jalgaon Market Area",
            "lat": 20.946000,
            "lng": 75.557000,
            "danger": False  # Previous alert (grey marker)
        }
    ]
    
    print(f"📍 Sending {len(jalgaon_locations)} alerts from Jalgaon locations...")
    print(f"🔴 Red markers: Current/danger alerts")
    print(f"⚪ Grey markers: Previous/safe alerts")
    print()
    
    success_count = 0
    
    for i, location in enumerate(jalgaon_locations, 1):
        alert_data = {
            "device_id": f"JALGAON_{i:02d}_{location['name'].replace(' ', '_').upper()}",
            "danger": location['danger'],
            "latitude": location['lat'],
            "longitude": location['lng']
        }
        
        status = "🚨 DANGER" if location['danger'] else "✅ SAFE"
        marker = "🔴 RED" if location['danger'] else "⚪ GREY"
        
        print(f"📡 {i}/{len(jalgaon_locations)} Sending: {location['name']}")
        print(f"   Status: {status} → {marker} marker")
        print(f"   Coords: {location['lat']}, {location['lng']}")
        
        try:
            response = requests.post(
                f"{backend_url}/api/alert",
                json=alert_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"   ✅ SUCCESS! Alert ID: {result.get('alert_id')}")
                success_count += 1
            else:
                print(f"   ❌ FAILED! Status: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("   ❌ CONNECTION ERROR!")
            print("   Make sure backend is running with: run_server.bat")
            break
            
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
        
        # Small delay between alerts
        if i < len(jalgaon_locations):
            time.sleep(1)
        print()
    
    print("=" * 40)
    print(f"📊 RESULTS: {success_count}/{len(jalgaon_locations)} alerts sent successfully")
    
    if success_count > 0:
        print("\n🔍 CHECK NOW:")
        print("1. 🌐 Web Dashboard: http://localhost:3000")
        print("   → Map should center on Jalgaon")
        print("   → Should show red and grey markers")
        print()
        print("2. 📱 Mobile App:")
        print("   → Should show 'Online' status")
        print("   → Should display all alerts")
        print()
        print("3. 🗺️  Map Markers:")
        print("   → Red markers = Current/danger alerts")
        print("   → Grey markers = Previous/safe alerts")
        
        print(f"\n📍 Map Center: Jalgaon, Maharashtra")
        print(f"   Coordinates: 20.947409, 75.554987")
    
    return success_count == len(jalgaon_locations)

if __name__ == "__main__":
    send_jalgaon_alerts()
    
    print("\n" + "=" * 40)
    input("Press Enter to exit...")