#!/usr/bin/env python3
"""
Test user registration and login
"""
import requests
import json
import time

def test_registration():
    print("🧪 Testing User Registration and Login...")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test user data
    test_user = {
        "name": "Test Guard",
        "phone": f"+91{int(time.time()) % 10000000000}",  # Unique phone number
        "password": "test123",  # Short, simple password
        "role": "guard"
    }
    
    try:
        # Test 1: Register user
        print("1. Testing user registration...")
        response = requests.post(
            f"{base_url}/api/auth/register",
            json=test_user,
            timeout=10
        )
        
        if response.status_code == 201:
            print(f"   ✅ Registration successful!")
            print(f"   📱 Phone: {test_user['phone']}")
            print(f"   👤 Name: {test_user['name']}")
            print(f"   🔐 Password: {test_user['password']}")
        else:
            print(f"   ❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        # Test 2: Login with the new user
        print("\n2. Testing user login...")
        login_data = {
            "phone": test_user["phone"],
            "password": test_user["password"]
        }
        
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Login successful!")
            print(f"   🎫 Token received: {data['access_token'][:20]}...")
            print(f"   👤 User: {data['user']['name']}")
            print(f"   📞 Phone: {data['user']['phone']}")
            print(f"   🏷️ Role: {data['user']['role']}")
        else:
            print(f"   ❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        print("\n" + "=" * 50)
        print("🎉 REGISTRATION AND LOGIN WORKING!")
        print("✅ User can register successfully")
        print("✅ User can login successfully") 
        print("✅ JWT tokens are generated")
        print("=" * 50)
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server")
        print("Make sure the backend is running on http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_registration()
    if success:
        print("\n🚀 Your authentication system is working!")
        print("Users can now register and login through the mobile app.")
    else:
        print("\n❌ Authentication test failed. Check the backend logs.")