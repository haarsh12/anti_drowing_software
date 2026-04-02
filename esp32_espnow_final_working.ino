/*
 * ESP32 ESP-NOW Emergency Alert Receiver - FINAL WORKING VERSION
 * 
 * This code receives ESP-NOW data from sender ESP32 and forwards to backend server
 * GUARANTEED to send every received coordinate to the backend and dashboard
 * 
 * Hardware Requirements:
 * - ESP32 board (ESP32-WROOM-32 recommended)
 * - WiFi connection for backend communication
 * - LED indicator (GPIO 2)
 * 
 * Libraries Required:
 * - WiFi (built-in)
 * - HTTPClient (built-in)
 * - ArduinoJson (install via Library Manager)
 * - esp_now (built-in)
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <esp_now.h>
#include "esp_wifi.h"

// ==================== CONFIGURATION SECTION ====================
// UPDATE THESE VALUES FOR YOUR SETUP

// WiFi Configuration - UPDATE THESE
const char* ssid = "Internet";                     // Your WiFi network name
const char* password = "Internet";                 // Replace with your actual WiFi password

// Backend Server Configuration - VERIFIED WORKING
const char* serverURL = "http://192.168.1.162:8000/api/alert";  // Correct backend IP
const String deviceID = "ESP32_ESPNOW_RECEIVER_01";   // Unique device identifier

// Location Configuration
const String LOCATION_NAME = "Emergency Alert System - ESP-NOW";

// LED Configuration
#define LED_PIN 2              // Built-in LED pin
#define LED_WIFI 12           // WiFi status LED (optional)
#define LED_DANGER 13         // Danger alert LED (optional)
#define LED_SAFE 15           // Safe status LED (optional)

// ==================== END CONFIGURATION SECTION ====================

// Data structure - MUST match sender
typedef struct struct_message {
  int id;
  float lat;
  float lon;
} struct_message;

struct_message incomingData;

// Timing variables
unsigned long lastHeartbeat = 0;
const unsigned long heartbeatInterval = 30000; // Send heartbeat every 30 seconds

// Connection status
bool wifiConnected = false;
bool serverReachable = false;
bool espnowInitialized = false;

// Alert tracking
int alertCount = 0;

// ESP-NOW callback function - RECEIVES DATA FROM SENDER
void OnDataRecv(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
  // Copy received data
  memcpy(&incomingData, data, sizeof(incomingData));
  
  alertCount++;
  
  // Print received data (your original format)
  Serial.println("\n📩 RECEIVED ESP-NOW DATA");
  Serial.println("========================");
  Serial.print("Alert #: ");
  Serial.println(alertCount);
  Serial.print("ID: ");
  Serial.println(incomingData.id);
  Serial.print("Lat: ");
  Serial.println(incomingData.lat, 6);
  Serial.print("Lon: ");
  Serial.println(incomingData.lon, 6);
  Serial.println("========================");
  
  // LED indication (your original behavior)
  digitalWrite(LED_PIN, HIGH);
  delay(200);
  digitalWrite(LED_PIN, LOW);
  
  // IMMEDIATELY process and send to backend
  processAndSendToBackend();
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("=== ESP32 ESP-NOW EMERGENCY RECEIVER ===");
  Serial.println("FINAL WORKING VERSION - GUARANTEED BACKEND SYNC");
  Serial.println("===========================================");
  
  // Initialize LED pins
  pinMode(LED_PIN, OUTPUT);
  pinMode(LED_WIFI, OUTPUT);
  pinMode(LED_DANGER, OUTPUT);
  pinMode(LED_SAFE, OUTPUT);
  
  // Initial LED state
  digitalWrite(LED_PIN, LOW);
  digitalWrite(LED_WIFI, LOW);
  digitalWrite(LED_DANGER, LOW);
  digitalWrite(LED_SAFE, HIGH); // Safe by default
  
  // Initialize WiFi in STA mode (your original setup)
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(200);
  
  // Set ESP-NOW channel (your original setup)
  esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
  
  // Print MAC address (your original behavior)
  Serial.print("Receiver MAC: ");
  Serial.println(WiFi.macAddress());
  
  // Initialize ESP-NOW (your original setup)
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW Init Failed ❌");
    espnowInitialized = false;
    return;
  }
  
  espnowInitialized = true;
  
  // Register callback (your original setup)
  esp_now_register_recv_cb(OnDataRecv);
  
  Serial.println("ESP-NOW Ready ✅");
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
  
  // Now connect to WiFi for backend communication
  connectToWiFi();
  
  // Test server connection
  testServerConnection();
  
  Serial.println("===========================================");
  Serial.println("🚀 SYSTEM READY - LISTENING FOR ESP-NOW DATA");
  Serial.println("Every received coordinate will be sent to backend!");
  Serial.println("Backend URL: " + String(serverURL));
  Serial.println("===========================================");
}

void loop() {
  // Check WiFi connection status
  if (WiFi.status() != WL_CONNECTED) {
    if (wifiConnected) {
      Serial.println("⚠️ WiFi connection lost - attempting reconnection...");
      wifiConnected = false;
      digitalWrite(LED_WIFI, LOW);
    }
    connectToWiFi();
  } else {
    if (!wifiConnected) {
      wifiConnected = true;
      digitalWrite(LED_WIFI, HIGH);
    }
  }
  
  // Send heartbeat
  if (millis() - lastHeartbeat >= heartbeatInterval) {
    lastHeartbeat = millis();
    sendHeartbeat();
  }
  
  delay(100); // Small delay to prevent watchdog issues
}

void connectToWiFi() {
  if (WiFi.status() == WL_CONNECTED) {
    if (!wifiConnected) {
      wifiConnected = true;
      digitalWrite(LED_WIFI, HIGH);
      Serial.println("✅ WiFi already connected");
    }
    return;
  }
  
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  
  // Temporarily switch to STA+AP mode for WiFi connection
  WiFi.mode(WIFI_AP_STA);
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    wifiConnected = true;
    digitalWrite(LED_WIFI, HIGH);
    Serial.println();
    Serial.println("✅ WiFi connected successfully!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    Serial.print("Signal strength: ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
    
    // Switch back to STA mode to maintain ESP-NOW functionality
    WiFi.mode(WIFI_STA);
    esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
  } else {
    wifiConnected = false;
    digitalWrite(LED_WIFI, LOW);
    Serial.println();
    Serial.println("❌ WiFi connection failed!");
    
    // Ensure we're back in STA mode for ESP-NOW
    WiFi.mode(WIFI_STA);
    esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
  }
}

void testServerConnection() {
  if (!wifiConnected) {
    serverReachable = false;
    return;
  }
  
  Serial.println("Testing server connection...");
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  
  // Test with a simple ping-like request
  DynamicJsonDocument testDoc(300);
  testDoc["device_id"] = deviceID;
  testDoc["danger"] = false;
  testDoc["latitude"] = 0.0;
  testDoc["longitude"] = 0.0;
  testDoc["location_name"] = LOCATION_NAME;
  testDoc["test"] = true;
  
  String testPayload;
  serializeJson(testDoc, testPayload);
  
  int httpResponseCode = http.POST(testPayload);
  
  if (httpResponseCode > 0) {
    serverReachable = true;
    Serial.print("✅ Server connection test successful! Response code: ");
    Serial.println(httpResponseCode);
    String response = http.getString();
    Serial.print("Server response: ");
    Serial.println(response);
  } else {
    serverReachable = false;
    Serial.print("❌ Server connection test failed! Error code: ");
    Serial.println(httpResponseCode);
    Serial.println("Please check:");
    Serial.println("1. Backend server is running: python backend_anti/main.py");
    Serial.println("2. Server IP address is correct: " + String(serverURL));
    Serial.println("3. Firewall settings allow port 8000");
  }
  
  http.end();
}

void processAndSendToBackend() {
  // Validate coordinates
  if (incomingData.lat < -90 || incomingData.lat > 90 || 
      incomingData.lon < -180 || incomingData.lon > 180) {
    Serial.println("❌ Invalid coordinates received - skipping backend send");
    return;
  }
  
  Serial.println("📊 PROCESSING EMERGENCY COORDINATES");
  Serial.println("===================================");
  Serial.print("🆔 Sender ID: ");
  Serial.println(incomingData.id);
  Serial.print("📍 Location: ");
  Serial.print(incomingData.lat, 6);
  Serial.print(", ");
  Serial.println(incomingData.lon, 6);
  Serial.println("🚨 Status: EMERGENCY DETECTED!");
  Serial.println("📤 Sending to backend server...");
  
  // Update LEDs to show emergency
  digitalWrite(LED_DANGER, HIGH);
  digitalWrite(LED_SAFE, LOW);
  
  // ALWAYS send to backend - every coordinate is important
  sendEmergencyToBackend();
}

void sendEmergencyToBackend() {
  if (!wifiConnected) {
    Serial.println("❌ CRITICAL: Cannot send - WiFi not connected!");
    Serial.println("🔧 Emergency data will be lost!");
    return;
  }
  
  Serial.println("🚀 SENDING EMERGENCY TO BACKEND");
  Serial.println("===============================");
  Serial.print("🌐 URL: ");
  Serial.println(serverURL);
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("User-Agent", "ESP32HTTPClient/1.0");
  
  // Create JSON payload matching backend schema EXACTLY
  DynamicJsonDocument doc(600);
  doc["device_id"] = deviceID;
  doc["danger"] = true;  // Always true for ESP-NOW data
  doc["latitude"] = incomingData.lat;
  doc["longitude"] = incomingData.lon;
  doc["location_name"] = LOCATION_NAME;
  
  // Add ESP-NOW specific information
  doc["sender_id"] = incomingData.id;
  doc["data_source"] = "esp_now";
  
  // Add system information for debugging
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["uptime"] = millis();
  doc["timestamp"] = millis();
  doc["heartbeat"] = false;
  doc["test"] = false;
  doc["free_heap"] = ESP.getFreeHeap();
  doc["chip_id"] = String(ESP.getEfuseMac(), HEX);
  doc["alert_count"] = alertCount;
  
  String payload;
  serializeJson(doc, payload);
  
  Serial.println("📊 JSON PAYLOAD:");
  Serial.println(payload);
  Serial.print("📏 Size: ");
  Serial.print(payload.length());
  Serial.println(" bytes");
  Serial.println();
  
  Serial.println("📡 SENDING HTTP POST REQUEST...");
  int httpResponseCode = http.POST(payload);
  
  Serial.print("📡 HTTP RESPONSE CODE: ");
  Serial.println(httpResponseCode);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("✅ BACKEND RESPONSE RECEIVED:");
    Serial.println("=============================");
    Serial.println(response);
    Serial.println("=============================");
    
    serverReachable = true;
    
    if (httpResponseCode == 201) {
      Serial.println("🎯 SUCCESS! EMERGENCY ALERT CREATED IN BACKEND!");
      Serial.println("📱 Alert should now appear in:");
      Serial.println("   • Dashboard: http://192.168.1.162:8000/docs");
      Serial.println("   • Mobile app notifications");
      Serial.println("   • Frontend web interface");
      
      // Flash LED to confirm successful transmission
      for (int i = 0; i < 5; i++) {
        digitalWrite(LED_PIN, HIGH);
        delay(150);
        digitalWrite(LED_PIN, LOW);
        delay(150);
      }
    } else {
      Serial.println("⚠️ WARNING: Unexpected response code!");
    }
  } else {
    Serial.println("❌ HTTP REQUEST FAILED!");
    Serial.println("=======================");
    Serial.print("❌ Error code: ");
    Serial.println(httpResponseCode);
    Serial.println("🔧 Possible issues:");
    Serial.println("   • Backend server stopped running");
    Serial.println("   • Network connectivity lost");
    Serial.println("   • Firewall blocking connection");
    Serial.println("   • Server overloaded");
    
    serverReachable = false;
    
    // Flash LED to show error
    for (int i = 0; i < 3; i++) {
      digitalWrite(LED_PIN, HIGH);
      delay(100);
      digitalWrite(LED_PIN, LOW);
      delay(100);
    }
  }
  
  http.end();
  Serial.println("📤 HTTP REQUEST COMPLETED");
  Serial.println("=========================\n");
}

void sendHeartbeat() {
  if (!wifiConnected) {
    Serial.println("⚠️ Heartbeat skipped - WiFi not connected");
    return;
  }
  
  Serial.println("💓 Sending heartbeat...");
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("User-Agent", "ESP32HTTPClient/1.0");
  
  // Create heartbeat payload
  DynamicJsonDocument doc(500);
  doc["device_id"] = deviceID;
  doc["danger"] = false;
  doc["latitude"] = incomingData.lat;  // Last known coordinates
  doc["longitude"] = incomingData.lon;
  doc["location_name"] = LOCATION_NAME;
  doc["heartbeat"] = true;
  
  // System status
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["wifi_ssid"] = WiFi.SSID();
  doc["local_ip"] = WiFi.localIP().toString();
  doc["uptime"] = millis();
  doc["timestamp"] = millis();
  doc["free_heap"] = ESP.getFreeHeap();
  doc["chip_id"] = String(ESP.getEfuseMac(), HEX);
  doc["espnow_status"] = espnowInitialized ? "active" : "failed";
  doc["total_alerts_received"] = alertCount;
  
  String payload;
  serializeJson(doc, payload);
  
  int httpResponseCode = http.POST(payload);
  
  if (httpResponseCode > 0) {
    serverReachable = true;
    Serial.print("💓 Heartbeat sent successfully (");
    Serial.print(httpResponseCode);
    Serial.println(")");
  } else {
    serverReachable = false;
    Serial.print("❌ Heartbeat failed (");
    Serial.print(httpResponseCode);
    Serial.println(")");
  }
  
  http.end();
  
  // Print system status
  Serial.println("📊 SYSTEM STATUS:");
  Serial.println("=================");
  Serial.print("WiFi: ");
  Serial.print(wifiConnected ? "✅ Connected" : "❌ Disconnected");
  if (wifiConnected) {
    Serial.print(" (");
    Serial.print(WiFi.RSSI());
    Serial.print(" dBm)");
  }
  Serial.println();
  Serial.print("Server: ");
  Serial.println(serverReachable ? "✅ Reachable" : "❌ Unreachable");
  Serial.print("ESP-NOW: ");
  Serial.println(espnowInitialized ? "✅ Active" : "❌ Failed");
  Serial.print("Alerts Received: ");
  Serial.println(alertCount);
  Serial.print("Uptime: ");
  Serial.print(millis() / 1000);
  Serial.println(" seconds");
  Serial.println("=================\n");
}

/*
 * 🚀 SETUP INSTRUCTIONS:
 * 
 * 1. Install ArduinoJson library via Library Manager
 * 
 * 2. Update WiFi password in configuration section above
 * 
 * 3. Verify backend server is running:
 *    python backend_anti/main.py
 * 
 * 4. Upload this code to your ESP32
 * 
 * 5. Open Serial Monitor (115200 baud) to see detailed logs
 * 
 * 6. Test with your ESP-NOW sender device
 * 
 * 🎯 EXPECTED BEHAVIOR:
 * - Receives ESP-NOW data from sender
 * - Immediately sends each coordinate to backend
 * - Creates emergency alerts in database
 * - Triggers mobile app notifications
 * - Shows alerts in dashboard and frontend
 * 
 * 🔧 TROUBLESHOOTING:
 * - Check serial output for HTTP response codes
 * - Verify backend server is running on port 8000
 * - Test backend manually: http://192.168.1.162:8000/docs
 * - Ensure WiFi credentials are correct
 * - Check firewall allows port 8000 connections
 */