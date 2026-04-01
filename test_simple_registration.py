#!/usr/bin/env python3
"""
Simple registration test with the exact same data as mobile app
"""
import requests
import json

def test_simple_registration():
    print("🧪 Testing Simple Registration...")
    print("=" * 40)
    
    # Use the same data as shown in the mobile app
    test_user = {
        "name": "Harsh",
        "phone": "8446117247",
        "password": "123456",  # Simple 6-digit password
        "role": "guard"
    }
    
    try:
        print(f"Testing registration with:")
        print(f"  Name: {test_user['name']}")
        print(f"  Phone: {test_user['phone']}")
        print(f"  Password: {test_user['password']}")
        print(f"  Role: {test_user['role']}")
        print()
        
        response = requests.post(
            "http://192.168.1.162:8000/api/auth/register",
            json=test_user,
            timeout=10
        )
        
        print(f"Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            return True
        elif response.status_code == 400 and "already registered" in response.text:
            print("⚠️ User already exists - trying login instead...")
            
            # Try login
            login_data = {
                "phone": test_user["phone"],
                "password": test_user["password"]
            }
            
            login_response = requests.post(
                "http://192.168.1.162:8000/api/auth/login",
                json=login_data,
                timeout=10
            )
            
            if login_response.status_code == 200:
                print("✅ Login successful!")
                return True
            else:
                print(f"❌ Login failed: {login_response.text}")
                return False
        else:
            print(f"❌ Registration failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_registration()
    if success:
        print("\n🎉 Backend registration is working!")
        print("The mobile app should work now.")
    else:
        print("\n❌ Backend registration still has issues.")
        print("Make sure you restarted the backend server.")