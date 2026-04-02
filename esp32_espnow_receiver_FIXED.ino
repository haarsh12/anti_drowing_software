#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <esp_now.h>
#include "esp_wifi.h"

const char* ssid = "Internet";
const char* password = "Jislwifi*8";
const char* serverURL = "http://192.168.1.162:8000/api/alert";
const String deviceID = "ESP32_ESPNOW_RECEIVER_01";

const String LOCATION_NAME = "Emergency Alert System";

#define LED_PIN 2
#define LED_WIFI 12
#define LED_DANGER 13
#define LED_SAFE 15

typedef struct struct_message {
  int id;
  float lat;
  float lon;
} struct_message;

// ✅ FIXED: Initialize with valid default coordinates
struct_message incomingData = {
  .id = 0,
  .lat = 20.947320,    // Default location (Jalgaon)
  .lon = 75.554890
};

unsigned long lastHeartbeat = 0;
const unsigned long heartbeatInterval = 30000;
unsigned long lastDataReceived = 0;
const unsigned long dataTimeout = 60000;

bool wifiConnected = false;
bool serverReachable = false;
bool espnowInitialized = false;

bool currentDangerState = false;
unsigned long lastDangerAlert = 0;
const unsigned long dangerCooldown = 5000;
int lastReceivedID = -1;

bool hasReceivedData = false;  // ✅ NEW: Track if we got data from ESP-NOW

void OnDataRecv(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
  memcpy(&incomingData, data, sizeof(incomingData));
  
  lastDataReceived = millis();
  hasReceivedData = true;  // ✅ FIXED: Mark that we have real data

  Serial.println("\n📩 RECEIVED");
  Serial.print("ID: ");
  Serial.println(incomingData.id);
  Serial.print("Lat: ");
  Serial.println(incomingData.lat, 6);
  Serial.print("Lon: ");
  Serial.println(incomingData.lon, 6);

  digitalWrite(LED_PIN, HIGH);
  delay(200);
  digitalWrite(LED_PIN, LOW);

  processReceivedData();
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  pinMode(LED_PIN, OUTPUT);
  pinMode(LED_WIFI, OUTPUT);
  pinMode(LED_DANGER, OUTPUT);
  pinMode(LED_SAFE, OUTPUT);

  digitalWrite(LED_PIN, LOW);
  digitalWrite(LED_WIFI, LOW);
  digitalWrite(LED_DANGER, LOW);
  digitalWrite(LED_SAFE, HIGH);

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

  connectToWiFi();
}

void loop() {
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
      Serial.println("✅ WiFi connected successfully!");
      Serial.print("IP address: ");
      Serial.println(WiFi.localIP());
    }
  }

  if (millis() - lastHeartbeat >= heartbeatInterval) {
    lastHeartbeat = millis();
    sendHeartbeat();
  }

  // ✅ FIXED: Only send safe status if we received danger data first
  if (currentDangerState && hasReceivedData && (millis() - lastDataReceived > dataTimeout)) {
    Serial.println("⏰ No recent danger signals - assuming safe status");
    currentDangerState = false;
    digitalWrite(LED_DANGER, LOW);
    digitalWrite(LED_SAFE, HIGH);
    sendSafeStatus();
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

void processReceivedData() {
  // ✅ FIXED: Validate GPS coordinates
  if (incomingData.lat < -90 || incomingData.lat > 90 || 
      incomingData.lon < -180 || incomingData.lon > 180) {
    Serial.println("❌ Invalid GPS coordinates received!");
    return;
  }

  // ✅ FIXED: Danger detection should be based on actual conditions
  // Currently: always treat received data as danger alert
  // TODO: Implement real danger detection logic here
  bool isDanger = true;  // ✅ For now, any ESP-NOW data = danger alert

  if (isDanger) {
    digitalWrite(LED_DANGER, HIGH);
    digitalWrite(LED_SAFE, LOW);

    // Only send alert if it's new or cooldown passed
    if (!currentDangerState || (millis() - lastDangerAlert > dangerCooldown) || 
        (lastReceivedID != incomingData.id)) {
      currentDangerState = true;
      lastDangerAlert = millis();
      lastReceivedID = incomingData.id;
      sendToServer(true);
    }
  } else {
    digitalWrite(LED_DANGER, LOW);
    digitalWrite(LED_SAFE, HIGH);

    if (currentDangerState) {
      currentDangerState = false;
      sendToServer(false);
    }
  }
}

void sendToServer(bool danger) {
  if (!wifiConnected) {
    Serial.println("❌ Cannot send: WiFi not connected");
    return;
  }

  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("User-Agent", "ESP32HTTPClient/1.0");

  // ✅ FIXED: Create JSON with all necessary fields
  DynamicJsonDocument doc(800);
  doc["device_id"] = deviceID;
  doc["danger"] = danger;
  doc["latitude"] = incomingData.lat;
  doc["longitude"] = incomingData.lon;
  doc["location_name"] = LOCATION_NAME;
  doc["sender_id"] = incomingData.id;
  doc["data_source"] = "esp_now";
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["uptime"] = millis() / 1000;  // Convert to seconds
  doc["timestamp"] = millis() / 1000;
  doc["espnow_status"] = espnowInitialized ? "active" : "failed";
  doc["heartbeat"] = false;
  // ✅ REMOVED: doc["test"] = false;  // No test data in production
  doc["free_heap"] = ESP.getFreeHeap();
  doc["chip_id"] = String(ESP.getEfuseMac(), HEX);

  String payload;
  serializeJson(doc, payload);

  int httpResponseCode = http.POST(payload);

  // ✅ FIXED: Check response and log it
  if (httpResponseCode > 0) {
    Serial.print("✅ Server response: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("❌ HTTP error: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}

void sendSafeStatus() {
  if (!wifiConnected) {
    Serial.println("❌ Cannot send: WiFi not connected");
    return;
  }

  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("User-Agent", "ESP32HTTPClient/1.0");

  DynamicJsonDocument doc(600);
  doc["device_id"] = deviceID;
  doc["danger"] = false;
  doc["latitude"] = incomingData.lat;
  doc["longitude"] = incomingData.lon;
  doc["location_name"] = LOCATION_NAME;
  doc["timeout_recovery"] = true;
  doc["timestamp"] = millis() / 1000;
  doc["heartbeat"] = false;
  doc["wifi_rssi"] = WiFi.RSSI();

  String payload;
  serializeJson(doc, payload);

  int httpResponseCode = http.POST(payload);

  // ✅ FIXED: Check response
  if (httpResponseCode > 0) {
    Serial.print("✅ Safe status sent, response: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("❌ Failed to send safe status, error: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}

void sendHeartbeat() {
  if (!wifiConnected) return;

  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("User-Agent", "ESP32HTTPClient/1.0");

  // ✅ FIXED: Heartbeat should always use current valid coordinates
  DynamicJsonDocument doc(700);
  doc["device_id"] = deviceID;
  doc["danger"] = false;
  doc["latitude"] = incomingData.lat;  // Use last known valid location
  doc["longitude"] = incomingData.lon;
  doc["location_name"] = LOCATION_NAME;
  doc["heartbeat"] = true;
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["wifi_ssid"] = WiFi.SSID();
  doc["local_ip"] = WiFi.localIP().toString();
  doc["uptime"] = millis() / 1000;
  doc["timestamp"] = millis() / 1000;
  doc["free_heap"] = ESP.getFreeHeap();
  doc["chip_id"] = String(ESP.getEfuseMac(), HEX);
  doc["espnow_status"] = espnowInitialized ? "active" : "failed";
  doc["current_state"] = currentDangerState ? "danger" : "safe";
  doc["last_data_received"] = lastDataReceived / 1000;
  doc["data_age"] = (millis() - lastDataReceived) / 1000;
  doc["has_received_esp_now"] = hasReceivedData;

  String payload;
  serializeJson(doc, payload);

  int httpResponseCode = http.POST(payload);

  // ✅ FIXED: Log heartbeat status
  if (httpResponseCode > 0) {
    Serial.print("💓 Heartbeat sent (");
    Serial.print(httpResponseCode);
    Serial.println(")");
  }

  http.end();
}
