#!/usr/bin/env python3
"""
Get IP Address for Mobile App Configuration
Helps users find their computer's IP address for mobile app backend connection
"""

import socket
import subprocess
import platform

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote server to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None

def get_all_ips():
    """Get all available IP addresses"""
    ips = []
    
    try:
        if platform.system() == "Windows":
            # Windows command
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if 'IPv4 Address' in line:
                    ip = line.split(':')[-1].strip()
                    if ip and not ip.startswith('127.'):
                        ips.append(ip)
        else:
            # Linux/Mac command
            result = subprocess.run(['ifconfig'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if 'inet ' in line and '127.0.0.1' not in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'inet' and i + 1 < len(parts):
                            ip = parts[i + 1]
                            if not ip.startswith('127.'):
                                ips.append(ip)
    except Exception as e:
        print(f"Error getting IPs: {e}")
    
    return ips

def main():
    print("🌐 IP ADDRESS CONFIGURATION FOR MOBILE APP")
    print("=" * 50)
    print("This script helps you find your computer's IP address")
    print("for configuring the mobile app backend connection.")
    print()
    
    # Get primary IP
    primary_ip = get_local_ip()
    if primary_ip:
        print(f"🎯 PRIMARY IP ADDRESS: {primary_ip}")
        print(f"   Use this in your mobile app configuration")
        print()
    
    # Get all IPs
    all_ips = get_all_ips()
    if all_ips:
        print("📋 ALL AVAILABLE IP ADDRESSES:")
        for i, ip in enumerate(all_ips, 1):
            print(f"   {i}. {ip}")
        print()
    
    # Configuration instructions
    print("📱 MOBILE APP CONFIGURATION:")
    print("=" * 50)
    print("1. Open: application_mobile/anti_drowing_app/lib/services/api_service.dart")
    print("2. Find the 'baseUrls' list")
    print("3. Add your IP address at the top:")
    print()
    if primary_ip:
        print("   static const List<String> baseUrls = [")
        print(f"     'http://{primary_ip}:8000',  // <-- Add this line")
        print("     'http://10.0.2.2:8000',")
        print("     'http://192.168.1.162:8000',")
        print("     'http://127.0.0.1:8000',")
        print("   ];")
    else:
        print("   static const List<String> baseUrls = [")
        print("     'http://YOUR_IP_HERE:8000',  // <-- Replace with your IP")
        print("     'http://10.0.2.2:8000',")
        print("     'http://192.168.1.162:8000',")
        print("     'http://127.0.0.1:8000',")
        print("   ];")
    print()
    
    # Testing instructions
    print("🧪 TESTING BACKEND CONNECTION:")
    print("=" * 50)
    if primary_ip:
        print(f"1. Test backend health: http://{primary_ip}:8000/health")
        print(f"2. Test API docs: http://{primary_ip}:8000/docs")
        print(f"3. Test alerts endpoint: http://{primary_ip}:8000/api/alerts")
    else:
        print("1. Test backend health: http://YOUR_IP:8000/health")
        print("2. Test API docs: http://YOUR_IP:8000/docs")
        print("3. Test alerts endpoint: http://YOUR_IP:8000/api/alerts")
    print()
    
    # Network requirements
    print("🔧 NETWORK REQUIREMENTS:")
    print("=" * 50)
    print("• Computer and mobile device must be on the same WiFi network")
    print("• Backend server must be running: python backend_anti/main.py")
    print("• Firewall should allow connections on port 8000")
    print("• Mobile device should have internet access")
    print()
    
    # Troubleshooting
    print("❌ TROUBLESHOOTING:")
    print("=" * 50)
    print("If mobile app can't connect:")
    print("1. Check both devices are on same WiFi")
    print("2. Try different IP addresses from the list above")
    print("3. Disable firewall temporarily for testing")
    print("4. Restart backend server")
    print("5. Check mobile app logs for connection errors")
    print()
    
    print("✅ After configuration, test with:")
    print("   python test_full_screen_notifications.py")

if __name__ == "__main__":
    main()