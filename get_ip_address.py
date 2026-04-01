#!/usr/bin/env python3
"""
Get IP Address for Mobile App Configuration
==========================================
This script helps you find your computer's IP address to configure the mobile app.
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
    except:
        return None

def get_all_ips():
    """Get all network interfaces and their IPs"""
    ips = []
    
    try:
        if platform.system() == "Windows":
            # Windows command
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            
            for line in lines:
                if 'IPv4 Address' in line and '192.168.' in line:
                    ip = line.split(':')[-1].strip()
                    if ip and ip != '127.0.0.1':
                        ips.append(ip)
        else:
            # Linux/Mac command
            result = subprocess.run(['ifconfig'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            
            for line in lines:
                if 'inet ' in line and '192.168.' in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == 'inet' and i + 1 < len(parts):
                            ip = parts[i + 1]
                            if ip != '127.0.0.1':
                                ips.append(ip)
    except:
        pass
    
    return ips

def main():
    print("🌐 IP Address Finder for Mobile App")
    print("=" * 40)
    
    # Get primary IP
    primary_ip = get_local_ip()
    if primary_ip:
        print(f"✅ Primary IP Address: {primary_ip}")
    
    # Get all IPs
    all_ips = get_all_ips()
    if all_ips:
        print(f"\n📋 All Network IPs found:")
        for i, ip in enumerate(all_ips, 1):
            print(f"   {i}. {ip}")
    
    print("\n📱 Mobile App Configuration:")
    print("=" * 40)
    
    if primary_ip:
        print(f"1. Open: application_mobile/anti_drowing_app/lib/services/api_service.dart")
        print(f"2. Replace 'http://192.168.1.100:8000' with 'http://{primary_ip}:8000'")
        print(f"3. Save the file and rebuild your mobile app")
        
        print(f"\n🔧 Your backend URL should be: http://{primary_ip}:8000")
        print(f"🌐 Your web dashboard URL: http://{primary_ip}:3000")
    else:
        print("❌ Could not detect IP address automatically")
        print("📝 Manual steps:")
        print("1. Open Command Prompt (Windows) or Terminal (Mac/Linux)")
        print("2. Run: ipconfig (Windows) or ifconfig (Mac/Linux)")
        print("3. Look for an IP address starting with 192.168.x.x")
        print("4. Use that IP in your mobile app configuration")
    
    print(f"\n⚠️  Important Notes:")
    print(f"- Make sure your phone and computer are on the same WiFi network")
    print(f"- Your backend must be running on: python -m uvicorn main:app --host 0.0.0.0 --port 8000")
    print(f"- Test the connection by opening http://YOUR_IP:8000 in your phone's browser")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")