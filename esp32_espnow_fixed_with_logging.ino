#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <esp_now.h>
#include "esp_wifi.h"

// Configuration
const char* ssid = "Internet";
const char* password = "Jislwifi*8";
const char* serverURL = "http://192.168.1.162:8000/api/alert";
const String deviceID = "ESP32_ESPNOW_RECEIVER_01";
const String LOCATION_NAME = "Emergency Alert System";

// LED pins
#define LED_PIN 2
#define LED_WIFI 12
#define LED_DANGER 13
#define LED_SAFE 15

// Data structure
typedef struct struct_message {
  int id;
  float lat;
  float lon;
} struct_message;

struct_message incomingData;

// Timing variables
unsigned long lastHeartbeat = 0;
const unsigned long heartbeatInterval = 30000;

// Connection status
bool wifiConnected = false;
bool serverReachable = false;
bool espnowInitialized = false;

// Alert tracking
int alertCount = 0;

// ESP-NOW callback function
void OnDataRecv(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
  memcpy(&incomingData, data, sizeof(incomingData));
  alertCount++;
  
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
  
  digitalWrite(LED_PIN, HIGH);
  delay(200);
  digitalWrite(LED_PIN, LOW);
  
  // IMMEDIATELY send to backend with detailed logging
  processAndSendToBackend();
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("=== ESP32 ESP-NOW EMERGENCY RECEIVER ===");
  Serial.println("WITH DETAILED BACKEND LOGGING");
  Serial.println("========================================");
  
  // Initialize LED pins
  pinMode(LED_PIN, OUTPUT);
  pinMode(LED_WIFI, OUTPUT);
  pinMode(LED_DANGER, OUTPUT);
  pinMode(LED_SAFE, OUTPUT);
  
  digitalWrite(LED_PIN, LOW);
  digitalWrite(LED_WIFI, LOW);
  digitalWrite(LED_DANGER, LOW);
  digitalWrite(LED_SAFE, HIGH);
  
  // Initialize WiFi and ESP-NOW
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(200);
  esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
  
  Serial.print("Receiver MAC: ");
  Serial.println(WiFi.macAddress());
  
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW Init Failed ❌");
    espnowInitialized = false;
    return;
  }
  
  espnowInitialized = true;
  esp_now_register_recv_cb(OnDataRecv);
  Serial.println("ESP-NOW Ready ✅");
  
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
  
  // Connect to WiFi
  connectToWiFi();
  
  // Test server connection
  testServerConnection();
  
  Serial.println("========================================");
  Serial.println("🚀 SYSTEM READY - LISTENING FOR DATA");
  Serial.println("Backend URL: " + String(serverURL));
  Serial.println("========================================");
}

void loop() {
  // Check WiFi connection
  if (WiFi.status() != WL_CONNECTED) {
    if (wifiConnected) {
      Serial.println("⚠️ WiFi connection lost - reconnecting...");
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
  
  delay(100);
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
    
    WiFi.mode(WIFI_STA);
    esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
  } else {
    wifiConnected = false;
    digitalWrite(LED_WIFI, LOW);
    Serial.println();
    Serial.println("❌ WiFi connection failed!");
    
    WiFi.mode(WIFI_STA);
    esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
  }
}

void testServerConnection() {
  if (!wifiConnected) {
    serverReachable = false;
    return;
  }
  
  Serial.println("🧪 Testing server connection...");
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  
  DynamicJsonDocument testDoc(300);
  testDoc["device_id"] = deviceID;
  testDoc["danger"] = false;
  testDoc["latitude"] = 0.0;
  testDoc["longitude"] = 0.0;
  testDoc["location_name"] = LOCATION_NAME;
  testDoc["test"] = true;
  
  String testPayload;
  serializeJson(testDoc, testPayload);
  
  Serial.print("📤 Sending test request to: ");
  Serial.println(serverURL);
  
  int httpResponseCode = http.POST(testPayload);
  
  Serial.print("📡 Test response code: ");
  Serial.println(httpResponseCode);
  
  if (httpResponseCode > 0) {
    serverReachable = true;
    String response = http.getString();
    Serial.print("✅ Server test successful! Response: ");
    Serial.println(response);
  } else {
    serverReachable = false;
    Serial.println("❌ Server test failed!");
    Serial.println("🔧 Check:");
    Serial.println("   1. Backend server running: python backend_anti/main.py");
    Serial.println("   2. IP address correct: " + String(serverURL));
    Serial.println("   3. Firewall allows port 8000");
  }
  
  http.end();
}

void processAndSendToBackend() {
  // Validate coordinates
  if (incomingData.lat < -90 || incomingData.lat > 90 || 
      incomingData.lon < -180 || incomingData.lon > 180) {
    Serial.println("❌ Invalid coordinates - skipping send");
    return;
  }
  
  Serial.println("\n🚨 PROCESSING EMERGENCY ALERT");
  Serial.println("==============================");
  Serial.print("🆔 Sender ID: ");
  Serial.println(incomingData.id);
  Serial.print("📍 Coordinates: ");
  Serial.print(incomingData.lat, 6);
  Serial.print(", ");
  Serial.println(incomingData.lon, 6);
  Serial.println("🚨 Status: EMERGENCY DETECTED!");
  
  // Update LEDs
  digitalWrite(LED_DANGER, HIGH);
  digitalWrite(LED_SAFE, LOW);
  
  // Send to backend with detailed logging
  sendEmergencyToBackend();
}

void sendEmergencyToBackend() {
  if (!wifiConnected) {
    Serial.println("❌ CRITICAL: WiFi not connected - data will be lost!");
    return;
  }
  
  Serial.println("\n🚀 SENDING TO BACKEND SERVER");
  Serial.println("============================");
  Serial.print("🌐 URL: ");
  Serial.println(serverURL);
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("User-Agent", "ESP32HTTPClient/1.0");
  
  // Create JSON payload
  DynamicJsonDocument doc(600);
  doc["device_id"] = deviceID;
  doc["danger"] = true;  // Always true for ESP-NOW emergency data
  doc["latitude"] = incomingData.lat;
  doc["longitude"] = incomingData.lon;
  doc["location_name"] = LOCATION_NAME;
  doc["sender_id"] = incomingData.id;
  doc["data_source"] = "esp_now";
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
  Serial.println("================");
  Serial.println(payload);
  Serial.print("📏 Payload size: ");
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
      Serial.println("🎯 SUCCESS! EMERGENCY ALERT CREATED!");
      Serial.println("📱 Alert will appear in:");
      Serial.println("   • Dashboard: http://192.168.1.162:8000/docs");
      Serial.println("   • Mobile app notifications");
      Serial.println("   • Frontend website");
      Serial.println("   • Supabase database");
      
      // Success LED flash
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
    Serial.println("   • Backend server not running");
    Serial.println("   • Network connectivity lost");
    Serial.println("   • Firewall blocking port 8000");
    Serial.println("   • Server overloaded");
    
    serverReachable = false;
    
    // Error LED flash
    for (int i = 0; i < 3; i++) {
      digitalWrite(LED_PIN, HIGH);
      delay(100);
      digitalWrite(LED_PIN, LOW);
      delay(100);
    }
  }
  
  http.end();
  Serial.println("📤 HTTP REQUEST COMPLETED\n");
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
  
  DynamicJsonDocument doc(500);
  doc["device_id"] = deviceID;
  doc["danger"] = false;
  doc["latitude"] = incomingData.lat;
  doc["longitude"] = incomingData.lon;
  doc["location_name"] = LOCATION_NAME;
  doc["heartbeat"] = true;
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
  Serial.print("Backend: ");
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
 * 1. This code is already configured with your WiFi credentials
 * 
 * 2. Make sure backend server is running:
 *    python backend_anti/main.py
 * 
 * 3. Upload this code to your ESP32
 * 
 * 4. Open Serial Monitor (115200 baud) for detailed logs
 * 
 * 🎯 WHAT YOU'LL SEE:
 * When ESP-NOW data is received, you'll see:
 * - "📩 RECEIVED ESP-NOW DATA" with coordinates
 * - "🚨 PROCESSING EMERGENCY ALERT" 
 * - "🚀 SENDING TO BACKEND SERVER"
 * - "📊 JSON PAYLOAD" showing exact data sent
 * - "📡 HTTP RESPONSE CODE: 201" (success)
 * - "✅ BACKEND RESPONSE RECEIVED" with server response
 * - "🎯 SUCCESS! EMERGENCY ALERT CREATED!"
 * 
 * 🔧 BACKEND INTEGRATION:
 * - Data is sent to Supabase via your backend
 * - Appears in dashboard at http://192.168.1.162:8000/docs
 * - Triggers mobile app notifications
 * - Shows on frontend website
 * 
 * 🚨 TROUBLESHOOTING:
 * - If you see "❌ HTTP REQUEST FAILED", check backend server
 * - If no "🚀 SENDING TO BACKEND" appears, ESP-NOW data isn't being received
 * - Check Serial Monitor for detailed error messages
 */