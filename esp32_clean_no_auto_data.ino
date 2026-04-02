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

// Connection status
bool wifiConnected = false;
bool espnowInitialized = false;
int alertCount = 0;

// ESP-NOW callback - ONLY FUNCTION THAT SENDS DATA
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
  
  // ONLY send data when ESP-NOW is received
  Serial.println("🚨 SENDING RED EMERGENCY ALERT!");
  sendEmergencyAlert();
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("=== ESP32 CLEAN - NO AUTO DATA ===");
  Serial.println("ONLY sends data when ESP-NOW received");
  Serial.println("===================================");
  
  pinMode(LED_PIN, OUTPUT);
  pinMode(LED_WIFI, OUTPUT);
  pinMode(LED_DANGER, OUTPUT);
  pinMode(LED_SAFE, OUTPUT);
  
  digitalWrite(LED_PIN, LOW);
  digitalWrite(LED_WIFI, LOW);
  digitalWrite(LED_DANGER, LOW);
  digitalWrite(LED_SAFE, HIGH);
  
  // Initialize ESP-NOW
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(200);
  esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
  
  Serial.print("Receiver MAC: ");
  Serial.println(WiFi.macAddress());
  
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW Init Failed ❌");
    return;
  }
  
  espnowInitialized = true;
  esp_now_register_recv_cb(OnDataRecv);
  Serial.println("ESP-NOW Ready ✅");
  
  // Connect to WiFi
  connectToWiFi();
  
  Serial.println("===================================");
  Serial.println("🚀 SYSTEM READY");
  Serial.println("✅ NO automatic data sending");
  Serial.println("✅ ONLY sends when ESP-NOW received");
  Serial.println("✅ Creates RED emergency alerts");
  Serial.println("===================================");
}

void loop() {
  // ONLY WiFi management - NO DATA SENDING
  if (WiFi.status() != WL_CONNECTED) {
    if (wifiConnected) {
      Serial.println("⚠️ WiFi lost - reconnecting...");
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
  
  // NO HEARTBEAT SENDING
  // NO AUTOMATIC DATA
  // COMPLETE SILENCE UNLESS ESP-NOW RECEIVED
  
  delay(1000); // Check WiFi every second
}

void connectToWiFi() {
  if (WiFi.status() == WL_CONNECTED) {
    if (!wifiConnected) {
      wifiConnected = true;
      digitalWrite(LED_WIFI, HIGH);
      Serial.println("✅ WiFi connected");
    }
    return;
  }
  
  Serial.print("Connecting to WiFi...");
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
    Serial.println("✅ WiFi connected!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
    
    WiFi.mode(WIFI_STA);
    esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
  } else {
    wifiConnected = false;
    digitalWrite(LED_WIFI, LOW);
    Serial.println();
    Serial.println("❌ WiFi failed!");
    
    WiFi.mode(WIFI_STA);
    esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
  }
}

void sendEmergencyAlert() {
  if (!wifiConnected) {
    Serial.println("❌ WiFi not connected - cannot send!");
    return;
  }
  
  Serial.println("🚀 SENDING RED EMERGENCY ALERT");
  Serial.println("===============================");
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("User-Agent", "ESP32HTTPClient/1.0");
  
  // RED EMERGENCY ALERT JSON
  DynamicJsonDocument doc(600);
  doc["device_id"] = deviceID;
  doc["danger"] = true;  // RED EMERGENCY
  doc["latitude"] = incomingData.lat;
  doc["longitude"] = incomingData.lon;
  doc["location_name"] = LOCATION_NAME;
  doc["sender_id"] = incomingData.id;
  doc["data_source"] = "esp_now";
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["uptime"] = millis();
  doc["timestamp"] = millis();
  doc["heartbeat"] = false;  // NOT heartbeat
  doc["test"] = false;       // NOT test
  doc["free_heap"] = ESP.getFreeHeap();
  doc["chip_id"] = String(ESP.getEfuseMac(), HEX);
  doc["alert_count"] = alertCount;
  
  String payload;
  serializeJson(doc, payload);
  
  Serial.println("📊 RED ALERT PAYLOAD:");
  Serial.println(payload);
  
  int httpResponseCode = http.POST(payload);
  Serial.print("📡 Response: ");
  Serial.println(httpResponseCode);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("✅ RED ALERT SENT!");
    Serial.println("Response: " + response);
    
    // Flash RED LED
    digitalWrite(LED_DANGER, HIGH);
    digitalWrite(LED_SAFE, LOW);
    for (int i = 0; i < 10; i++) {
      digitalWrite(LED_PIN, HIGH);
      delay(100);
      digitalWrite(LED_PIN, LOW);
      delay(100);
    }
  } else {
    Serial.println("❌ FAILED to send!");
  }
  
  http.end();
  Serial.println("📤 COMPLETED\n");
}

/*
 * 🚨 GUARANTEED NO AUTOMATIC DATA
 * 
 * This code will:
 * ✅ NEVER send automatic data
 * ✅ ONLY send when ESP-NOW received
 * ✅ Create RED emergency alerts
 * ✅ Show exact coordinates
 * 
 * Upload this code and you will see:
 * • Complete silence when no ESP-NOW data
 * • RED alerts only when ESP-NOW received
 * • No heartbeat entries in backend
 */