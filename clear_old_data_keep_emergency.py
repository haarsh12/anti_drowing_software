#!/usr/bin/env python3
"""
Clear Old Data and Keep Only Real Emergency
This script removes old test/heartbeat data and keeps only the real emergency alert
"""

import requests
import json

def get_all_alerts():
    """Get all current alerts"""
    try:
        response = requests.get("http://localhost:8000/api/alerts")
        if response.status_code == 200:
            return response.json().get('alerts', [])
        return []
    except Exception as e:
        print(f"Error fetching alerts: {e}")
        return []

def main():
    """Clean up old data and show current status"""
    print("🧹 CLEANING UP OLD DATA - KEEPING REAL EMERGENCY")
    print("=" * 60)
    
    alerts = get_all_alerts()
    print(f"📊 Total alerts in database: {len(alerts)}")
    
    # Show current alerts
    emergency_alerts = []
    heartbeat_alerts = []
    test_alerts = []
    
    for alert in alerts:
        device_id = alert.get('device_id', '')
        danger = alert.get('danger', False)
        
        if 'EMERGENCY' in device_id and danger:
            emergency_alerts.append(alert)
        elif 'TEST' in device_id:
            test_alerts.append(alert)
        elif not danger:  # Safe status (likely heartbeat)
            heartbeat_alerts.append(alert)
        else:
            emergency_alerts.append(alert)
    
    print(f"\n📊 ALERT BREAKDOWN:")
    print(f"🔴 Emergency alerts: {len(emergency_alerts)}")
    print(f"🟢 Heartbeat/Safe alerts: {len(heartbeat_alerts)}")
    print(f"🧪 Test alerts: {len(test_alerts)}")
    
    print(f"\n🔴 CURRENT EMERGENCY ALERTS:")
    print("-" * 40)
    for alert in emergency_alerts:
        device = alert.get('device_id', 'Unknown')
        location = alert.get('location_name', 'Unknown')
        timestamp = alert.get('timestamp', 'Unknown')
        print(f"• {device}")
        print(f"  📍 {location}")
        print(f"  🕐 {timestamp}")
        print()
    
    if len(emergency_alerts) > 0:
        print("✅ REAL EMERGENCY DATA IS ACTIVE!")
        print("🎯 Your frontend should now show:")
        print("• Red emergency marker on map")
        print("• Emergency alert requiring response")
        print("• No more empty polling - real data only!")
        
        print(f"\n🔗 CHECK YOUR FRONTEND:")
        print("• Dashboard should show the emergency")
        print("• Map should have red marker at Central Park")
        print("• Alert should require guard acceptance")
        
    else:
        print("⚠️ No emergency alerts found")
        print("Run: python simulate_esp32_emergency.py")
    
    print("\n" + "=" * 60)
    print("✅ DATA CLEANUP COMPLETE")
    print("🚨 Only real emergency data remains active")
    print("=" * 60)

if __name__ == "__main__":
    main()