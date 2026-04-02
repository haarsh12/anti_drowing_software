#!/usr/bin/env python3
"""
Setup Jalgaon Emergency Data
Creates realistic emergency alerts within 30 meters of Jalgaon coordinates
"""

import requests
import json
import time
import random
import math
from datetime import datetime, timedelta

# Configuration
BACKEND_URL = "http://localhost:8000/api/alert"
CLEAR_URL = "http://localhost:8000/api/alerts/clear-all"

# Jalgaon target coordinates
JALGAON_CENTER_LAT = 20.947388232880304
JALGAON_CENTER_LON = 75.55519775066064

# Location names in Jalgaon area
JALGAON_LOCATIONS = [
    "Jalgaon Swimming Pool - Main Area",
    "Jalgaon Water Sports Center",
    "Jalgaon Municipal Pool - Deep End",
    "Jalgaon Aquatic Center - Training Pool",
    "Jalgaon Community Pool - Children's Area",
    "Jalgaon Sports Complex - Pool Zone",
    "Jalgaon Recreation Center - Pool",
    "Jalgaon Public Pool - Emergency Zone"
]

def generate_coordinates_within_radius(center_lat, center_lon, radius_meters):
    """Generate random coordinates within specified radius"""
    # Convert radius from meters to degrees (approximate)
    # 1 degree ≈ 111,000 meters at equator
    radius_deg = radius_meters / 111000.0
    
    # Generate random angle and distance
    angle = random.uniform(0, 2 * math.pi)
    distance = random.uniform(0, radius_deg)
    
    # Calculate new coordinates
    lat = center_lat + (distance * math.cos(angle))
    lon = center_lon + (distance * math.sin(angle))
    
    return lat, lon

def clear_existing_data():
    """Clear existing alerts (requires admin auth - will skip if not available)"""
    print("🧹 Attempting to clear existing data...")
    
    try:
        # Try to clear (may fail if no admin auth, that's okay)
        response = requests.delete(CLEAR_URL, timeout=5)
        if response.status_code == 200:
            print("✅ Existing data cleared successfully")
            return True
        else:
            print("⚠️ Could not clear existing data (admin auth required)")
            print("💡 New alerts will be added alongside existing ones")
            return False
    except Exception as e:
        print(f"⚠️ Could not clear existing data: {e}")
        print("💡 New alerts will be added alongside existing ones")
        return False

def create_jalgaon_emergency_alerts():
    """Create realistic emergency alerts in Jalgaon area"""
    
    print(f"\n🚨 CREATING JALGAON EMERGENCY ALERTS")
    print("=" * 50)
    print(f"📍 Center coordinates: {JALGAON_CENTER_LAT:.6f}, {JALGAON_CENTER_LON:.6f}")
    print(f"📏 Radius: 30 meters")
    print()
    
    alerts_created = []
    
    # Create 3-5 emergency alerts within 30 meters
    num_alerts = random.randint(3, 5)
    
    for i in range(num_alerts):
        # Generate coordinates within 30 meters
        lat, lon = generate_coordinates_within_radius(
            JALGAON_CENTER_LAT, 
            JALGAON_CENTER_LON, 
            30  # 30 meters radius
        )
        
        # Select random location name
        location_name = random.choice(JALGAON_LOCATIONS)
        
        # Create emergency data
        emergency_data = {
            "device_id": f"ESP32_JALGAON_DEVICE_{i+1:02d}",
            "danger": True,  # All are emergency alerts
            "latitude": lat,
            "longitude": lon,
            "location_name": location_name,
            
            # ESP32 specific fields
            "wifi_rssi": random.randint(-65, -35),  # Good to excellent signal
            "uptime": random.randint(50000, 500000),  # Various uptimes
            "timestamp": int(time.time() * 1000) - random.randint(0, 3600000),  # Within last hour
            "heartbeat": False,
            "test": False,
            "free_heap": random.randint(200000, 300000),
            "chip_id": f"240AC4{random.randint(100000, 999999):06d}",
            "data_source": "esp_now",
            "sender_id": random.randint(10000, 99999),
            "alert_count": i + 1
        }
        
        print(f"📡 Creating Alert #{i+1}:")
        print(f"   Device: {emergency_data['device_id']}")
        print(f"   Location: {location_name}")
        print(f"   Coordinates: {lat:.6f}, {lon:.6f}")
        
        # Calculate distance from center
        distance = math.sqrt(
            (lat - JALGAON_CENTER_LAT)**2 + (lon - JALGAON_CENTER_LON)**2
        ) * 111000  # Convert to meters
        print(f"   Distance from center: {distance:.1f} meters")
        
        try:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "ESP32HTTPClient/1.0"
            }
            
            response = requests.post(
                BACKEND_URL,
                json=emergency_data,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 201:
                print(f"   ✅ Success! Alert ID: {response.json()['data']['id']}")
                alerts_created.append(emergency_data)
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
        time.sleep(0.5)  # Small delay between requests
    
    return alerts_created

def create_safe_status_alerts():
    """Create a few safe status alerts for context"""
    
    print(f"🟢 CREATING SAFE STATUS ALERTS")
    print("-" * 30)
    
    # Create 2-3 safe status alerts
    for i in range(2):
        lat, lon = generate_coordinates_within_radius(
            JALGAON_CENTER_LAT, 
            JALGAON_CENTER_LON, 
            50  # Slightly wider radius for safe alerts
        )
        
        safe_data = {
            "device_id": f"ESP32_JALGAON_SAFE_{i+1:02d}",
            "danger": False,  # Safe status
            "latitude": lat,
            "longitude": lon,
            "location_name": f"Jalgaon Safe Zone {i+1}",
            "wifi_rssi": random.randint(-60, -40),
            "uptime": random.randint(100000, 600000),
            "timestamp": int(time.time() * 1000) - random.randint(7200000, 86400000),  # 2-24 hours ago
            "heartbeat": True,  # This is a heartbeat/status update
            "test": False,
            "free_heap": random.randint(250000, 350000),
            "chip_id": f"240AC5{random.randint(100000, 999999):06d}",
            "data_source": "esp_now"
        }
        
        print(f"   Safe Alert #{i+1}: {safe_data['location_name']}")
        
        try:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "ESP32HTTPClient/1.0"
            }
            
            response = requests.post(BACKEND_URL, json=safe_data, headers=headers, timeout=10)
            if response.status_code == 201:
                print(f"   ✅ Created")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

def verify_map_setup():
    """Verify the alerts are properly set up"""
    
    print(f"\n🔍 VERIFYING JALGAON MAP SETUP")
    print("=" * 40)
    
    try:
        response = requests.get("http://localhost:8000/api/alerts", timeout=5)
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            emergency_alerts = [a for a in alerts if a.get('danger', False)]
            safe_alerts = [a for a in alerts if not a.get('danger', False)]
            
            print(f"📊 Total alerts: {len(alerts)}")
            print(f"🔴 Emergency alerts: {len(emergency_alerts)}")
            print(f"🟢 Safe alerts: {len(safe_alerts)}")
            
            if emergency_alerts:
                print(f"\n🔴 EMERGENCY ALERTS IN JALGAON:")
                for alert in emergency_alerts[:5]:  # Show first 5
                    device = alert.get('device_id', 'Unknown')
                    location = alert.get('location_name', 'Unknown')
                    lat = alert.get('latitude', 0)
                    lon = alert.get('longitude', 0)
                    
                    # Calculate distance from center
                    distance = math.sqrt(
                        (lat - JALGAON_CENTER_LAT)**2 + (lon - JALGAON_CENTER_LON)**2
                    ) * 111000
                    
                    print(f"   • {device}")
                    print(f"     📍 {location}")
                    print(f"     📏 {distance:.1f}m from center")
                    print(f"     🗺️  {lat:.6f}, {lon:.6f}")
                    print()
            
            return True
        else:
            print(f"❌ Could not fetch alerts: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying setup: {e}")
        return False

def main():
    """Main setup function"""
    
    print("🗺️  JALGAON EMERGENCY MAP SETUP")
    print("=" * 60)
    print("Setting up realistic emergency data for Jalgaon area")
    print(f"📍 Target coordinates: {JALGAON_CENTER_LAT:.6f}, {JALGAON_CENTER_LON:.6f}")
    print(f"📏 Emergency alerts within 30 meters")
    print()
    
    # Step 1: Clear existing data (optional)
    clear_existing_data()
    
    # Step 2: Create emergency alerts
    alerts_created = create_jalgaon_emergency_alerts()
    
    # Step 3: Create some safe status alerts for context
    create_safe_status_alerts()
    
    # Step 4: Verify setup
    if verify_map_setup():
        print("=" * 60)
        print("✅ JALGAON MAP SETUP COMPLETE!")
        print("=" * 60)
        print()
        print("🎯 WHAT'S READY:")
        print("• Multiple emergency alerts within 30m of your coordinates")
        print("• Realistic Jalgaon location names")
        print("• Map will center on Jalgaon area")
        print("• Red emergency markers on map")
        print("• Safe status alerts for context")
        print()
        print("🔗 CHECK YOUR FRONTEND:")
        print("• Dashboard should show Jalgaon map")
        print("• Multiple red emergency markers")
        print("• All alerts within 30 meters of target")
        print("• Realistic location names")
        print()
        print("📍 MAP CENTER:")
        print(f"• Latitude: {JALGAON_CENTER_LAT:.6f}")
        print(f"• Longitude: {JALGAON_CENTER_LON:.6f}")
        print("• Zoom level: 13 (neighborhood view)")
        print()
        print("🚨 All emergency alerts require immediate response!")
        
    else:
        print("❌ Setup verification failed")
        print("Please check your backend is running and try again")

if __name__ == "__main__":
    main()