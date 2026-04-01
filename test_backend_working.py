#!/usr/bin/env python3
"""
Quick test to verify backend is working
"""
import requests
import json

def test_backend():
    print("🧪 Testing Backend Server...")
    print("=" * 40)
    
    try:
        # Test basic connectivity
        response = requests.get("http://localhost:8000/api/alerts", timeout=5)
        
        if response.status_code == 200:
            print("✅ Backend is working!")
            data = response.json()
            print(f"📊 Current alerts: {data.get('total', 0)}")
            print(f"🔗 API URL: http://localhost:8000")
            print(f"📚 Documentation: http://localhost:8000/docs")
            return True
        else:
            print(f"⚠️ Backend responded with status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend")
        print("Make sure the server is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_backend()