/*
 * ESP32 Multi-Protocol Receiver + Backend Forwarder
 * Receives from NRF24L01+PA+LNA and LoRa, forwards to backend
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <RF24.h>
#include <LoRa.h>

// WiFi Configuration
const char* ssid = "Internet";
const char* password = "Internet";

// Backend Configuration
const char* serverURL = "http://192.168.1.162:8000/api/alert";
const String deviceID = "ESP32_MULTI_RECEIVER_01";

// Pin Definitions
#define NRF_CE_PIN 4
#define NRF_CSN_PIN 5
#define LORA_SS_PIN 18
#define LORA_RST_PIN 14
#define LORA_DIO0_PIN 26
#define LED_NRF_PIN 12
#define LED_LORA_PIN 13
#define LED_WIFI_PIN 15
#define LED_EMERGENCY_PIN 2

// Module Initialization
RF24 radio(NRF_CE_PIN, NRF_CSN_PIN);

// NRF24L01 Configuration
const byte address[6] = "00001";
const uint8_t channel = 76;

// LoRa Configuration
const long loraFreq = 433E6;
const int loraSF = 12;
const long loraBW = 125E3;

// Data Structure (must match sender)
struct SensorData {
  uint32_t deviceId;
  float latitude;
  float longitude;
  float accelX, accelY, accelZ;
  float gyroX, gyroY, gyroZ;
  int16_t temperature;
  bool emergencyDetected;
  bool buttonPressed;
  uint32_t timestamp;
  uint8_t batteryLevel;
  int8_t rssi;
};

SensorData receivedData;
bool wifiConnected = false;
unsigned long lastHeartbeat = 0;
int packetsReceived = 0;

void setup() {
  Serial.begin(115200);
  
  // Initialize LEDs
  pinMode(LED_NRF_PIN, OUTPUT);
  pinMode(LED_LORA_PIN, OUTPUT);
  pinMode(LED_WIFI_PIN, OUTPUT);
  pinMode(LED_EMERGENCY_PIN, OUTPUT);
  
  // Initialize modules
  initNRF24();
  initLoRa();
  connectWiFi();
  
  Serial.println("Multi-Protocol Receiver Ready");
  blinkAllLEDs();
}

void loop() {
  // Check WiFi connection
  if (WiFi.status() != WL_CONNECTED) {
    wifiConnected = false;
    digitalWrite(LED_WIFI_PIN, LOW);
    connectWiFi();
  } else if (!wifiConnected) {
    wifiConnected = true;
    digitalWrite(LED_WIFI_PIN, HIGH);
  }
  
  // Check for NRF24L01 data
  if (radio.available()) {
    receiveNRF24Data();
  }
  
  // Check for LoRa data
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    receiveLoRaData(packetSize);
  }
  
  // Send heartbeat every 30 seconds
  if (millis() - lastHeartbeat > 30000) {
    sendHeartbeat();
    lastHeartbeat = millis();
  }
  
  delay(10);
}

void initNRF24() {
  if (!radio.begin()) {
    Serial.println("NRF24L01 init failed");
    return;
  }
  
  radio.openReadingPipe(0, address);
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(channel);
  radio.setDataRate(RF24_250KBPS);
  radio.setCRCLength(RF24_CRC_16);
  radio.setAutoAck(true);
  radio.startListening();
  
  Serial.println("NRF24L01 Ready");
  digitalWrite(LED_NRF_PIN, HIGH);
}

void initLoRa() {
  LoRa.setPins(LORA_SS_PIN, LORA_RST_PIN, LORA_DIO0_PIN);
  
  if (!LoRa.begin(loraFreq)) {
    Serial.println("LoRa init failed");
    return;
  }
  
  LoRa.setSpreadingFactor(loraSF);
  LoRa.setSignalBandwidth(loraBW);
  LoRa.setCodingRate4(8);
  LoRa.setPreambleLength(8);
  LoRa.setSyncWord(0x12);
  LoRa.enableCrc();
  
  Serial.println("LoRa Ready");
  digitalWrite(LED_LORA_PIN, HIGH);
}

void connectWiFi() {
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    wifiConnected = true;
    digitalWrite(LED_WIFI_PIN, HIGH);
    Serial.println();
    Serial.print("WiFi connected: ");
    Serial.println(WiFi.localIP());
  } else {
    wifiConnected = false;
    digitalWrite(LED_WIFI_PIN, LOW);
    Serial.println(" Failed!");
  }
}

void receiveNRF24Data() {
  radio.read(&receivedData, sizeof(receivedData));
  packetsReceived++;
  
  Serial.println("\n=== NRF24L01 DATA RECEIVED ===");
  printSensorData();
  
  // Visual indication
  blinkLED(LED_NRF_PIN, 2);
  
  // Forward to backend
  forwardToBackend("nrf24l01");
}

void receiveLoRaData(int packetSize) {
  if (packetSize == sizeof(SensorData)) {
    LoRa.readBytes((uint8_t*)&receivedData, sizeof(receivedData));
    packetsReceived++;
    
    Serial.println("\n=== LORA DATA RECEIVED ===");
    Serial.print("RSSI: "); Serial.println(LoRa.packetRssi());
    Serial.print("SNR: "); Serial.println(LoRa.packetSnr());
    printSensorData();
    
    // Visual indication
    blinkLED(LED_LORA_PIN, 2);
    
    // Forward to backend
    forwardToBackend("lora");
  }
}

void forwardToBackend(String protocol) {
  if (!wifiConnected) {
    Serial.println("Cannot forward - WiFi not connected");
    return;
  }
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("User-Agent", "ESP32MultiReceiver/1.0");
  
  // Create JSON payload
  DynamicJsonDocument doc(1024);
  doc["device_id"] = String(receivedData.deviceId, HEX);
  doc["danger"] = receivedData.emergencyDetected || receivedData.buttonPressed;
  doc["latitude"] = receivedData.latitude;
  doc["longitude"] = receivedData.longitude;
  doc["location_name"] = "Jalgaon Emergency Zone - " + protocol.toUpperCase();
  
  // Sensor data
  doc["accel_x"] = receivedData.accelX;
  doc["accel_y"] = receivedData.accelY;
  doc["accel_z"] = receivedData.accelZ;
  doc["gyro_x"] = receivedData.gyroX;
  doc["gyro_y"] = receivedData.gyroY;
  doc["gyro_z"] = receivedData.gyroZ;
  doc["temperature"] = receivedData.temperature;
  doc["battery_level"] = receivedData.batteryLevel;
  doc["button_pressed"] = receivedData.buttonPressed;
  
  // System info
  doc["protocol"] = protocol;
  doc["receiver_id"] = deviceID;
  doc["packets_received"] = packetsReceived;
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["uptime"] = millis();
  doc["timestamp"] = receivedData.timestamp;
  doc["heartbeat"] = false;
  doc["test"] = false;
  
  String payload;
  serializeJson(doc, payload);
  
  Serial.println("Forwarding to backend...");
  int httpResponseCode = http.POST(payload);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.print("Backend response: ");
    Serial.println(httpResponseCode);
    
    if (httpResponseCode == 201) {
      Serial.println("SUCCESS: Alert created in backend");
      
      // Emergency indication
      if (receivedData.emergencyDetected || receivedData.buttonPressed) {
        activateEmergencyAlert();
      }
    }
  } else {
    Serial.print("Backend request failed: ");
    Serial.println(httpResponseCode);
  }
  
  http.end();
}

void sendHeartbeat() {
  if (!wifiConnected) return;
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("User-Agent", "ESP32MultiReceiver/1.0");
  
  DynamicJsonDocument doc(512);
  doc["device_id"] = deviceID;
  doc["danger"] = false;
  doc["latitude"] = 20.947388;
  doc["longitude"] = 75.555198;
  doc["location_name"] = "Multi-Protocol Receiver Station";
  doc["heartbeat"] = true;
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["uptime"] = millis();
  doc["packets_received"] = packetsReceived;
  doc["nrf24_status"] = "active";
  doc["lora_status"] = "active";
  doc["free_heap"] = ESP.getFreeHeap();
  
  String payload;
  serializeJson(doc, payload);
  
  int httpResponseCode = http.POST(payload);
  Serial.print("Heartbeat: ");
  Serial.println(httpResponseCode > 0 ? "OK" : "Failed");
  
  http.end();
}

void activateEmergencyAlert() {
  Serial.println("EMERGENCY ALERT ACTIVATED!");
  
  // Flash emergency LED
  for (int i = 0; i < 10; i++) {
    digitalWrite(LED_EMERGENCY_PIN, HIGH);
    delay(100);
    digitalWrite(LED_EMERGENCY_PIN, LOW);
    delay(100);
  }
}

void printSensorData() {
  Serial.print("Device ID: 0x"); Serial.println(receivedData.deviceId, HEX);
  Serial.print("GPS: "); Serial.print(receivedData.latitude, 6);
  Serial.print(", "); Serial.println(receivedData.longitude, 6);
  Serial.print("Accel: "); Serial.print(receivedData.accelX);
  Serial.print(", "); Serial.print(receivedData.accelY);
  Serial.print(", "); Serial.println(receivedData.accelZ);
  Serial.print("Gyro: "); Serial.print(receivedData.gyroX);
  Serial.print(", "); Serial.print(receivedData.gyroY);
  Serial.print(", "); Serial.println(receivedData.gyroZ);
  Serial.print("Temperature: "); Serial.println(receivedData.temperature);
  Serial.print("Emergency: "); Serial.println(receivedData.emergencyDetected ? "YES" : "NO");
  Serial.print("Button: "); Serial.println(receivedData.buttonPressed ? "PRESSED" : "NORMAL");
  Serial.print("Battery: "); Serial.print(receivedData.batteryLevel); Serial.println("%");
  Serial.print("Timestamp: "); Serial.println(receivedData.timestamp);
  Serial.println("============================");
}

void blinkLED(int pin, int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(pin, HIGH);
    delay(100);
    digitalWrite(pin, LOW);
    delay(100);
  }
}

void blinkAllLEDs() {
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_NRF_PIN, HIGH);
    digitalWrite(LED_LORA_PIN, HIGH);
    digitalWrite(LED_WIFI_PIN, HIGH);
    digitalWrite(LED_EMERGENCY_PIN, HIGH);
    delay(200);
    digitalWrite(LED_NRF_PIN, LOW);
    digitalWrite(LED_LORA_PIN, LOW);
    digitalWrite(LED_WIFI_PIN, LOW);
    digitalWrite(LED_EMERGENCY_PIN, LOW);
    delay(200);
  }
}