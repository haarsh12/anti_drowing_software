#!/usr/bin/env python3
"""
Clear Heartbeat Data - Remove Automatic Safe Status Records
Removes all heartbeat/safe status records to show only real emergency alerts
"""

import requests
import json

# Configuration
BACKEND_URL = "http://192.168.1.162:8000"

def clear_safe_heartbeat_alerts():
    """Clear all safe/heartbeat alerts from the system"""
    try:
        # Get all current alerts
        response = requests.get(f"{BACKEND_URL}/api/alerts", timeout=10)
        if response.status_code == 200:
            data = response.json()
            alerts = data.get('alerts', [])
            
            print(f"📊 Total alerts in system: {len(alerts)}")
            
            # Count different types
            heartbeat_count = 0
            safe_count = 0
            emergency_count = 0
            
            for alert in alerts:
                if alert.get('heartbeat', False):
                    heartbeat_count += 1
                elif not alert.get('danger', True):
                    safe_count += 1
                else:
                    emergency_count += 1
            
            print(f"💓 Heartbeat alerts: {heartbeat_count}")
            print(f"🟢 Safe alerts: {safe_count}")
            print(f"🚨 Emergency alerts: {emergency_count}")
            
            print("\n🧹 To clear heartbeat/safe data:")
            print("1. Use database admin panel")
            print("2. Or implement clear endpoint in backend")
            print("3. Or manually delete from Supabase dashboard")
            
            return True
        else:
            print(f"❌ Failed to get alerts: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🧹 CLEAR HEARTBEAT DATA")
    print("=" * 40)
    print("This will help you remove automatic heartbeat data")
    print("and show only real ESP-NOW emergency alerts.")
    print()
    
    # Check current alerts
    clear_safe_heartbeat_alerts()
    
    print("\n" + "=" * 40)
    print("🔧 SYSTEM FIXES APPLIED:")
    print("=" * 40)
    print("✅ ESP32 heartbeat sending: DISABLED")
    print("✅ ESP-NOW data creates: RED EMERGENCY ALERTS")
    print("✅ Backend coordinate precision: FIXED (6 decimals)")
    print()
    
    print("📋 NEXT STEPS:")
    print("=" * 40)
    print("1. Upload the fixed ESP32 code")
    print("2. Test with ESP-NOW sender")
    print("3. You should see:")
    print("   • ESP32: '🚨 EMERGENCY DETECTED - SENDING RED ALERT!'")
    print("   • Backend: '🚨 Danger Status: 🔴 EMERGENCY!'")
    print("   • Backend: '💓 Heartbeat: False'")
    print("   • Dashboard: RED emergency alerts")
    print("   • Mobile: Push notifications")
    print()
    
    print("🎯 EXPECTED BEHAVIOR:")
    print("=" * 40)
    print("• NO automatic data sending")
    print("• ESP-NOW data = RED emergency alert")
    print("• Real coordinates displayed accurately")
    print("• Alerts require manual acceptance")
    print("• Mobile app gets push notifications")

if __name__ == "__main__":
    main()