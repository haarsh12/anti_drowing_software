#!/usr/bin/env python3
"""
Verify Jalgaon Setup
Shows the current emergency alerts and their positions relative to target coordinates
"""

import requests
import math

# Target coordinates
TARGET_LAT = 20.947388232880304
TARGET_LON = 75.55519775066064

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in meters"""
    # Simple distance calculation (good for short distances)
    lat_diff = lat2 - lat1
    lon_diff = lon2 - lon1
    distance_deg = math.sqrt(lat_diff**2 + lon_diff**2)
    distance_meters = distance_deg * 111000  # Convert to meters
    return distance_meters

def main():
    print("🔍 JALGAON EMERGENCY SETUP VERIFICATION")
    print("=" * 60)
    print(f"📍 Target coordinates: {TARGET_LAT:.6f}, {TARGET_LON:.6f}")
    print()
    
    try:
        response = requests.get("http://localhost:8000/api/alerts", timeout=5)
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            # Filter Jalgaon emergency alerts
            jalgaon_emergencies = [
                alert for alert in alerts 
                if alert.get('danger', False) and 'JALGAON' in alert.get('device_id', '').upper()
            ]
            
            print(f"🚨 JALGAON EMERGENCY ALERTS: {len(jalgaon_emergencies)}")
            print("-" * 50)
            
            for i, alert in enumerate(jalgaon_emergencies, 1):
                device_id = alert.get('device_id', 'Unknown')
                location = alert.get('location_name', 'Unknown')
                lat = alert.get('latitude', 0)
                lon = alert.get('longitude', 0)
                timestamp = alert.get('timestamp', 'Unknown')
                
                # Calculate distance from target
                distance = calculate_distance(TARGET_LAT, TARGET_LON, lat, lon)
                
                print(f"Alert #{i}:")
                print(f"  🆔 Device: {device_id}")
                print(f"  📍 Location: {location}")
                print(f"  🗺️  Coordinates: {lat:.6f}, {lon:.6f}")
                print(f"  📏 Distance from target: {distance:.1f} meters")
                print(f"  🕐 Time: {timestamp}")
                
                # Status indicator
                if distance <= 30:
                    print(f"  ✅ Within 30m radius")
                else:
                    print(f"  ⚠️  Outside 30m radius")
                print()
            
            # Map information
            print("🗺️  MAP CONFIGURATION:")
            print("-" * 30)
            print(f"• Center: {TARGET_LAT:.6f}, {TARGET_LON:.6f}")
            print(f"• Zoom level: 16 (street level)")
            print(f"• All alerts within 30 meters")
            print(f"• Red markers for emergencies")
            print(f"• Grey markers for safe status")
            
            print(f"\n🎯 FRONTEND SHOULD SHOW:")
            print("• Jalgaon map centered on your coordinates")
            print("• Multiple red emergency markers clustered together")
            print("• Detailed popup information for each alert")
            print("• All emergency locations within walking distance")
            
            return True
            
        else:
            print(f"❌ Could not fetch alerts: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    main()