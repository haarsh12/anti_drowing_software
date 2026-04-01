#!/usr/bin/env python3
"""
Emergency System Test Script
============================
This script simulates ESP32 emergency signals to test the complete system:
ESP32 → Backend → Web Dashboard → Mobile App

Usage:
    python test_emergency_system.py
"""

import requests
import json
import time
import random
from datetime import datetime
from typing import Dict, Any

class EmergencySystemTester:
    def __init__(self, backend_url: str = "http://127.0.0.1:8000"):
        self.backend_url = backend_url
        self.test_results = []
        
    def print_header(self, title: str):
        """Print a formatted header"""
        print("\n" + "="*60)
        print(f"🚨 {title}")
        print("="*60)
    
    def print_step(self, step: str, status: str = "INFO"):
        """Print a test step"""
        icons = {"INFO": "ℹ️", "SUCCESS": "✅", "ERROR": "❌", "WARNING": "⚠️"}
        print(f"{icons.get(status, 'ℹ️')} {step}")
    
    def test_backend_connection(self) -> bool:
        """Test if backend is running and accessible"""
        self.print_header("Testing Backend Connection")
        
        try:
            response = requests.get(f"{self.backend_url}/", timeout=5)
            if response.status_code == 200:
                self.print_step("Backend is running and accessible", "SUCCESS")
                return True
            else:
                self.print_step(f"Backend returned status code: {response.status_code}", "ERROR")
                return False
        except requests.exceptions.RequestException as e:
            self.print_step(f"Cannot connect to backend: {e}", "ERROR")
            self.print_step("Make sure your backend is running on http://127.0.0.1:8000", "WARNING")
            return False
    
    def get_current_alerts(self) -> Dict[str, Any]:
        """Get current alerts from backend"""
        try:
            response = requests.get(f"{self.backend_url}/api/alerts", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"alerts": [], "total": 0}
        except:
            return {"alerts": [], "total": 0}
    
    def send_mock_emergency_alert(self, device_id: str, danger: bool = True, 
                                 latitude: float = None, longitude: float = None) -> bool:
        """Send a mock emergency alert (simulating ESP32)"""
        
        # Generate random coordinates if not provided
        if latitude is None:
            latitude = round(random.uniform(40.7000, 40.7500), 6)  # NYC area
        if longitude is None:
            longitude = round(random.uniform(-74.0200, -73.9500), 6)  # NYC area
        
        alert_data = {
            "device_id": device_id,
            "danger": danger,
            "latitude": latitude,
            "longitude": longitude
        }
        
        try:
            response = requests.post(
                f"{self.backend_url}/api/alert",
                json=alert_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 201:
                result = response.json()
                self.print_step(f"Emergency alert sent successfully! Alert ID: {result.get('alert_id')}", "SUCCESS")
                self.print_step(f"Device: {device_id}, Danger: {danger}, Location: ({latitude}, {longitude})")
                return True
            else:
                self.print_step(f"Failed to send alert. Status: {response.status_code}", "ERROR")
                self.print_step(f"Response: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            self.print_step(f"Network error sending alert: {e}", "ERROR")
            return False
    
    def run_single_test(self):
        """Run a single emergency test"""
        self.print_header("Single Emergency Alert Test")
        
        device_id = f"ESP32_TEST_{int(time.time())}"
        success = self.send_mock_emergency_alert(device_id, danger=True)
        
        if success:
            self.print_step("✅ Check your web dashboard - you should see the new alert!")
            self.print_step("✅ Check your mobile app - it should refresh and show the alert!")
            
            # Wait and show current alerts
            time.sleep(2)
            alerts = self.get_current_alerts()
            self.print_step(f"Total alerts in system: {alerts.get('total', 0)}")
        
        return success
    
    def run_multiple_tests(self, count: int = 3):
        """Run multiple emergency tests"""
        self.print_header(f"Multiple Emergency Alerts Test ({count} alerts)")
        
        success_count = 0
        
        for i in range(count):
            self.print_step(f"Sending alert {i+1}/{count}...")
            
            device_id = f"ESP32_DEVICE_{i+1:03d}"
            danger = random.choice([True, False])  # Random danger level
            
            if self.send_mock_emergency_alert(device_id, danger):
                success_count += 1
            
            # Wait between alerts
            if i < count - 1:
                time.sleep(1)
        
        self.print_step(f"Successfully sent {success_count}/{count} alerts", 
                       "SUCCESS" if success_count == count else "WARNING")
        
        # Show final status
        time.sleep(2)
        alerts = self.get_current_alerts()
        self.print_step(f"Total alerts in system: {alerts.get('total', 0)}")
        
        return success_count == count
    
    def run_stress_test(self, count: int = 10, delay: float = 0.5):
        """Run stress test with many alerts"""
        self.print_header(f"Stress Test ({count} alerts with {delay}s delay)")
        
        success_count = 0
        start_time = time.time()
        
        for i in range(count):
            device_id = f"STRESS_TEST_{i+1:03d}"
            danger = i % 2 == 0  # Alternate between danger and safe
            
            if self.send_mock_emergency_alert(device_id, danger):
                success_count += 1
            
            if i < count - 1:
                time.sleep(delay)
        
        end_time = time.time()
        duration = end_time - start_time
        
        self.print_step(f"Stress test completed in {duration:.2f} seconds")
        self.print_step(f"Success rate: {success_count}/{count} ({success_count/count*100:.1f}%)")
        
        return success_count == count
    
    def run_location_test(self):
        """Test with specific locations"""
        self.print_header("Location-Based Emergency Test")
        
        # Test locations (famous places)
        locations = [
            {"name": "Central Park, NYC", "lat": 40.7829, "lng": -73.9654},
            {"name": "Brooklyn Bridge, NYC", "lat": 40.7061, "lng": -73.9969},
            {"name": "Times Square, NYC", "lat": 40.7580, "lng": -73.9855},
            {"name": "Statue of Liberty, NYC", "lat": 40.6892, "lng": -74.0445},
        ]
        
        success_count = 0
        
        for i, location in enumerate(locations):
            self.print_step(f"Sending emergency from {location['name']}...")
            device_id = f"LOCATION_TEST_{i+1}"
            
            if self.send_mock_emergency_alert(
                device_id, 
                danger=True, 
                latitude=location['lat'], 
                longitude=location['lng']
            ):
                success_count += 1
            
            time.sleep(1)
        
        self.print_step(f"Location test completed: {success_count}/{len(locations)} alerts sent")
        return success_count == len(locations)
    
    def show_system_status(self):
        """Show current system status"""
        self.print_header("System Status")
        
        # Get current alerts
        alerts = self.get_current_alerts()
        total_alerts = alerts.get('total', 0)
        
        self.print_step(f"Total alerts in database: {total_alerts}")
        
        if total_alerts > 0:
            recent_alerts = alerts.get('alerts', [])[:5]  # Show last 5
            self.print_step("Recent alerts:")
            
            for alert in recent_alerts:
                device = alert.get('device_id', 'Unknown')
                danger = "🚨 DANGER" if alert.get('danger') else "✅ SAFE"
                timestamp = alert.get('timestamp', 'Unknown time')
                self.print_step(f"  - {device}: {danger} at {timestamp}")
        
        # Test web dashboard
        self.print_step("🌐 Web Dashboard: http://localhost:3000")
        self.print_step("📱 Mobile App: Check your device")
        self.print_step("🖥️  Backend API: http://127.0.0.1:8000/api/alerts")
    
    def run_full_test_suite(self):
        """Run complete test suite"""
        self.print_header("🚨 EMERGENCY SYSTEM FULL TEST SUITE 🚨")
        
        # Check backend connection first
        if not self.test_backend_connection():
            self.print_step("Cannot proceed without backend connection", "ERROR")
            return False
        
        # Run all tests
        tests = [
            ("Single Alert Test", lambda: self.run_single_test()),
            ("Multiple Alerts Test", lambda: self.run_multiple_tests(3)),
            ("Location Test", lambda: self.run_location_test()),
            ("Stress Test", lambda: self.run_stress_test(5, 0.3)),
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                result = test_func()
                results.append((test_name, result))
                time.sleep(2)  # Pause between tests
            except Exception as e:
                self.print_step(f"Test '{test_name}' failed with error: {e}", "ERROR")
                results.append((test_name, False))
        
        # Show final results
        self.print_header("Test Results Summary")
        
        passed = 0
        for test_name, result in results:
            status = "PASSED" if result else "FAILED"
            icon = "✅" if result else "❌"
            self.print_step(f"{test_name}: {status}", "SUCCESS" if result else "ERROR")
            if result:
                passed += 1
        
        self.print_step(f"Overall: {passed}/{len(results)} tests passed")
        
        # Show system status
        self.show_system_status()
        
        return passed == len(results)

def main():
    """Main function"""
    print("🚨 Emergency System Tester")
    print("=" * 40)
    print("This script will test your complete emergency response system:")
    print("ESP32 Simulation → Backend → Web Dashboard → Mobile App")
    print()
    
    # Initialize tester
    tester = EmergencySystemTester()
    
    # Show menu
    while True:
        print("\n📋 Test Options:")
        print("1. Single Emergency Alert Test")
        print("2. Multiple Alerts Test (3 alerts)")
        print("3. Location-Based Test")
        print("4. Stress Test (5 rapid alerts)")
        print("5. Full Test Suite (All tests)")
        print("6. Show System Status")
        print("7. Exit")
        
        try:
            choice = input("\nSelect test (1-7): ").strip()
            
            if choice == "1":
                tester.run_single_test()
            elif choice == "2":
                tester.run_multiple_tests(3)
            elif choice == "3":
                tester.run_location_test()
            elif choice == "4":
                tester.run_stress_test(5, 0.3)
            elif choice == "5":
                tester.run_full_test_suite()
            elif choice == "6":
                tester.show_system_status()
            elif choice == "7":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-7.")
                
        except KeyboardInterrupt:
            print("\n👋 Test interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()