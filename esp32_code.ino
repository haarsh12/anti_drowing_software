/*
 * ESP32 LoRa Emergency Alert System - PRODUCTION READY
 * 
 * This code receives LoRa data in format: "danger,latitude,longitude"
 * and sends it to the backend server via HTTP POST request
 * 
 * Hardware Requirements:
 * - ESP32 board (ESP32-WROOM-32 recommended)
 * - LoRa module (SX1276/SX1278)
 * - WiFi connection
 * - LED indicators (optional)
 * 
 * Libraries Required:
 * - WiFi (built-in)
 * - HTTPClient (built-in)
 * - ArduinoJson (install via Library Manager)
 * - LoRa by Sandeep Mistry (install via Library Manager)
 * 
 * CONFIGURATION INSTRUCTIONS:
 * 1. Update WiFi credentials below
 * 2. Update server URL with your backend IP address
 * 3. Verify LoRa pin connections match your hardware
 * 4. Upload code to ESP32
 * 5. Monitor Serial output for connection status
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <LoRa.h>
#include <SPI.h>

// ==================== CONFIGURATION SECTION ====================
// UPDATE THESE VALUES FOR YOUR SETUP

// WiFi Configuration - CHANGE THESE
const char* ssid = "YOUR_WIFI_SSID";           // Replace with your WiFi network name
const char* password = "YOUR_WIFI_PASSWORD";   // Replace with your WiFi password

// Backend Server Configuration - CHANGE THIS
const char* serverURL = "http://192.168.1.100:8000/api/alert";  // Replace with your server IP
const String deviceID = "ESP32_RECEIVER_01";   // Unique device identifier

// LoRa Configuration - VERIFY PIN CONNECTIONS
#define SS 5      // LoRa chip select pin (GPIO 5)
#define RST 14    // LoRa reset pin (GPIO 14)
#define DIO0 2    // LoRa DIO0 pin (GPIO 2)
#define FREQUENCY 433E6  // LoRa frequency (433MHz - check local regulations)

// LED pins for status indication (optional)
#define LED_WIFI 12    // WiFi status LED (GPIO 12)
#define LED_DANGER 13  // Danger alert LED (GPIO 13)
#define LED_SAFE 15    // Safe status LED (GPIO 15)

// ==================== END CONFIGURATION SECTION ====================

// Timing variables
unsigned long lastHeartbeat = 0;
const unsigned long heartbeatInterval = 30000; // Send heartbeat every 30 seconds
unsigned long lastLoRaCheck = 0;
const unsigned long loraCheckInterval = 1000;  // Check LoRa every 1 second

// Connection status
bool wifiConnected = false;
bool serverReachable = false;

void setup() {
  Serial.begin(115200);
  Serial.println("=== ESP32 LoRa Emergency Alert System ===");
  Serial.println("Version: 2.0 - Production Ready");
  Serial.println("==========================================");
  
  // Initialize LED pins
  pinMode(LED_WIFI, OUTPUT);
  pinMode(LED_DANGER, OUTPUT);
  pinMode(LED_SAFE, OUTPUT);
  
  // Initial LED state - all off
  digitalWrite(LED_WIFI, LOW);
  digitalWrite(LED_DANGER, LOW);
  digitalWrite(LED_SAFE, HIGH); // Safe LED on by default
  
  // Initialize LoRa
  Serial.println("Initializing LoRa...");
  LoRa.setPins(SS, RST, DIO0);
  
  if (!LoRa.begin(FREQUENCY)) {
    Serial.println("❌ LoRa initialization failed!");
    while (1) {
      // Blink all LEDs to indicate error
      digitalWrite(LED_WIFI, HIGH);
      digitalWrite(LED_DANGER, HIGH);
      digitalWrite(LED_SAFE, HIGH);
      delay(500);
      digitalWrite(LED_WIFI, LOW);
      digitalWrite(LED_DANGER, LOW);
      digitalWrite(LED_SAFE, LOW);
      delay(500);
    }
  }
  
  Serial.println("✅ LoRa initialized successfully");
  Serial.print("Frequency: ");
  Serial.print(FREQUENCY / 1000000);
  Serial.println(" MHz");
  
  // Connect to WiFi
  connectToWiFi();
  
  // Test server connection
  testServerConnection();
  
  Serial.println("==========================================");
  Serial.println("🚀 System ready - Listening for LoRa data...");
  Serial.println("Expected format: 'danger,latitude,longitude'");
  Serial.println("Example: '1,20.9517,75.1681' or '0,20.9517,75.1681'");
  Serial.println("==========================================");
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
  }
  
  // Check for LoRa packets
  if (millis() - lastLoRaCheck >= loraCheckInterval) {
    lastLoRaCheck = millis();
    checkForLoRaData();
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
  } else {
    wifiConnected = false;
    digitalWrite(LED_WIFI, LOW);
    Serial.println();
    Serial.println("❌ WiFi connection failed!");
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
  DynamicJsonDocument testDoc(200);
  testDoc["device_id"] = deviceID;
  testDoc["danger"] = false;
  testDoc["latitude"] = 0.0;
  testDoc["longitude"] = 0.0;
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
    Serial.println("1. Server IP address in serverURL");
    Serial.println("2. Server is running and accessible");
    Serial.println("3. Firewall settings");
  }
  
  http.end();
}

void checkForLoRaData() {
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String receivedData = "";
    
    // Read packet
    while (LoRa.available()) {
      receivedData += (char)LoRa.read();
    }
    
    // Get RSSI
    int rssi = LoRa.packetRssi();
    
    Serial.println("📡 LoRa packet received!");
    Serial.print("Data: ");
    Serial.println(receivedData);
    Serial.print("RSSI: ");
    Serial.print(rssi);
    Serial.println(" dBm");
    
    // Parse and send data
    parseAndSendData(receivedData, rssi);
  }
}

void parseAndSendData(String data, int rssi) {
  // Expected format: "danger,latitude,longitude"
  // Example: "1,20.9517,75.1681" or "0,20.9517,75.1681"
  
  int firstComma = data.indexOf(',');
  int secondComma = data.indexOf(',', firstComma + 1);
  
  if (firstComma == -1 || secondComma == -1) {
    Serial.println("❌ Invalid data format received!");
    Serial.println("Expected format: 'danger,latitude,longitude'");
    return;
  }
  
  String dangerStr = data.substring(0, firstComma);
  String latStr = data.substring(firstComma + 1, secondComma);
  String lonStr = data.substring(secondComma + 1);
  
  // Convert to appropriate types
  bool danger = (dangerStr.toInt() == 1);
  double latitude = latStr.toDouble();
  double longitude = lonStr.toDouble();
  
  // Validate coordinates (basic check)
  if (latitude < -90 || latitude > 90 || longitude < -180 || longitude > 180) {
    Serial.println("❌ Invalid coordinates received!");
    Serial.print("Latitude: ");
    Serial.print(latitude);
    Serial.print(", Longitude: ");
    Serial.println(longitude);
    return;
  }
  
  Serial.println("📊 Parsed data:");
  Serial.print("Danger: ");
  Serial.println(danger ? "YES" : "NO");
  Serial.print("Latitude: ");
  Serial.println(latitude, 6);
  Serial.print("Longitude: ");
  Serial.println(longitude, 6);
  
  // Update LEDs based on danger status
  if (danger) {
    digitalWrite(LED_DANGER, HIGH);
    digitalWrite(LED_SAFE, LOW);
    Serial.println("🚨 DANGER DETECTED - Sending emergency alert!");
  } else {
    digitalWrite(LED_DANGER, LOW);
    digitalWrite(LED_SAFE, HIGH);
    Serial.println("✅ Safe status - Sending normal update");
  }
  
  // Send to server
  sendToServer(danger, latitude, longitude, rssi);
}

void sendToServer(bool danger, double latitude, double longitude, int rssi) {
  if (!wifiConnected) {
    Serial.println("❌ Cannot send - WiFi not connected");
    return;
  }
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  
  // Create JSON payload
  DynamicJsonDocument doc(300);
  doc["device_id"] = deviceID;
  doc["danger"] = danger;
  doc["latitude"] = latitude;
  doc["longitude"] = longitude;
  doc["rssi"] = rssi;
  doc["timestamp"] = millis();
  
  String payload;
  serializeJson(doc, payload);
  
  Serial.println("📤 Sending to server...");
  Serial.print("URL: ");
  Serial.println(serverURL);
  Serial.print("Payload: ");
  Serial.println(payload);
  
  int httpResponseCode = http.POST(payload);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.print("✅ Server response code: ");
    Serial.println(httpResponseCode);
    Serial.print("Response: ");
    Serial.println(response);
    
    serverReachable = true;
    
    if (danger) {
      Serial.println("🚨 EMERGENCY ALERT SENT SUCCESSFULLY!");
      // Flash danger LED to confirm
      for (int i = 0; i < 5; i++) {
        digitalWrite(LED_DANGER, LOW);
        delay(100);
        digitalWrite(LED_DANGER, HIGH);
        delay(100);
      }
    }
  } else {
    Serial.print("❌ HTTP Error code: ");
    Serial.println(httpResponseCode);
    serverReachable = false;
    
    // Try to reconnect on next heartbeat
    Serial.println("Will retry on next heartbeat...");
  }
  
  http.end();
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
  
  // Create heartbeat payload
  DynamicJsonDocument doc(250);
  doc["device_id"] = deviceID;
  doc["danger"] = false;
  doc["latitude"] = 0.0;
  doc["longitude"] = 0.0;
  doc["heartbeat"] = true;
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["uptime"] = millis();
  
  String payload;
  serializeJson(doc, payload);
  
  int httpResponseCode = http.POST(payload);
  
  if (httpResponseCode > 0) {
    serverReachable = true;
    Serial.print("💓 Heartbeat sent successfully (");
    Serial.print(httpResponseCode);
    Serial.println(")");
    
    // Test server connection if it was previously unreachable
    if (!serverReachable) {
      testServerConnection();
    }
  } else {
    serverReachable = false;
    Serial.print("❌ Heartbeat failed (");
    Serial.print(httpResponseCode);
    Serial.println(")");
  }
  
  http.end();
  
  // Print system status
  Serial.println("📊 System Status:");
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
  Serial.print("Uptime: ");
  Serial.print(millis() / 1000);
  Serial.println(" seconds");
  Serial.println("==========================================");
}
  
  // Initialize LED pins
  pinMode(LED_WIFI, OUTPUT);
  pinMode(LED_DANGER, OUTPUT);
  pinMode(LED_SAFE, OUTPUT);
  
  // Turn off all LEDs initially
  digitalWrite(LED_WIFI, LOW);
  digitalWrite(LED_DANGER, LOW);
  digitalWrite(LED_SAFE, LOW);
  
  // Initialize LoRa
  initLoRa();
  
  // Connect to WiFi
  connectToWiFi();
  
  Serial.println("System ready!");
  digitalWrite(LED_SAFE, HIGH); // Indicate system is ready
}

void loop() {
  // Check WiFi connection
  if (WiFi.status() != WL_CONNECTED) {
    digitalWrite(LED_WIFI, LOW);
    Serial.println("WiFi disconnected. Reconnecting...");
    connectToWiFi();
  } else {
    digitalWrite(LED_WIFI, HIGH);
  }
  
  // Check for LoRa messages
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    String receivedData = "";
    
    // Read the packet
    while (LoRa.available()) {
      receivedData += (char)LoRa.read();
    }
    
    Serial.println("Received LoRa data: " + receivedData);
    
    // Process the received data
    processLoRaData(receivedData);
  }
  
  // Send periodic heartbeat (safe status)
  if (millis() - lastHeartbeat > heartbeatInterval) {
    sendHeartbeat();
    lastHeartbeat = millis();
  }
  
  delay(100); // Small delay to prevent excessive CPU usage
}

void initLoRa() {
  Serial.println("Initializing LoRa...");
  
  // Set LoRa pins
  LoRa.setPins(SS, RST, DIO0);
  
  // Initialize LoRa with frequency
  if (!LoRa.begin(FREQUENCY)) {
    Serial.println("Starting LoRa failed!");
    while (1) {
      // Blink danger LED to indicate LoRa failure
      digitalWrite(LED_DANGER, HIGH);
      delay(200);
      digitalWrite(LED_DANGER, LOW);
      delay(200);
    }
  }
  
  // Set LoRa parameters
  LoRa.setSpreadingFactor(7);    // SF7 for faster transmission
  LoRa.setSignalBandwidth(125E3); // 125kHz bandwidth
  LoRa.setCodingRate4(5);        // 4/5 coding rate
  LoRa.setPreambleLength(8);     // 8 symbol preamble
  LoRa.setSyncWord(0x12);        // Sync word
  
  Serial.println("LoRa initialized successfully!");
}

void connectToWiFi() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.println("WiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    digitalWrite(LED_WIFI, HIGH);
  } else {
    Serial.println();
    Serial.println("WiFi connection failed!");
    digitalWrite(LED_WIFI, LOW);
  }
}

void processLoRaData(String data) {
  // Expected format: "danger,latitude,longitude"
  // Example: "1,18.52,73.85" or "0,18.52,73.85"
  
  int firstComma = data.indexOf(',');
  int secondComma = data.indexOf(',', firstComma + 1);
  
  if (firstComma == -1 || secondComma == -1) {
    Serial.println("Invalid data format received");
    return;
  }
  
  // Parse the data
  String dangerStr = data.substring(0, firstComma);
  String latStr = data.substring(firstComma + 1, secondComma);
  String lonStr = data.substring(secondComma + 1);
  
  bool isDanger = (dangerStr == "1" || dangerStr.equalsIgnoreCase("true"));
  float latitude = latStr.toFloat();
  float longitude = lonStr.toFloat();
  
  // Validate coordinates
  if (latitude < -90 || latitude > 90 || longitude < -180 || longitude > 180) {
    Serial.println("Invalid coordinates received");
    return;
  }
  
  Serial.println("Parsed data:");
  Serial.println("  Danger: " + String(isDanger ? "YES" : "NO"));
  Serial.println("  Latitude: " + String(latitude, 6));
  Serial.println("  Longitude: " + String(longitude, 6));
  
  // Update LED status
  if (isDanger) {
    digitalWrite(LED_DANGER, HIGH);
    digitalWrite(LED_SAFE, LOW);
  } else {
    digitalWrite(LED_DANGER, LOW);
    digitalWrite(LED_SAFE, HIGH);
  }
  
  // Send data to server
  sendAlertToServer(isDanger, latitude, longitude);
}

void sendAlertToServer(bool danger, float latitude, float longitude) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi not connected. Cannot send data.");
    return;
  }
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  
  // Create JSON payload
  StaticJsonDocument<200> jsonDoc;
  jsonDoc["device_id"] = deviceID;
  jsonDoc["danger"] = danger;
  jsonDoc["latitude"] = latitude;
  jsonDoc["longitude"] = longitude;
  
  String jsonString;
  serializeJson(jsonDoc, jsonString);
  
  Serial.println("Sending to server: " + jsonString);
  
  // Send POST request
  int httpResponseCode = http.POST(jsonString);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("Server response code: " + String(httpResponseCode));
    Serial.println("Server response: " + response);
    
    if (httpResponseCode == 201) {
      Serial.println("Alert sent successfully!");
      // Brief flash to indicate successful transmission
      for (int i = 0; i < 3; i++) {
        digitalWrite(LED_WIFI, LOW);
        delay(100);
        digitalWrite(LED_WIFI, HIGH);
        delay(100);
      }
    }
  } else {
    Serial.println("Error sending data. HTTP error code: " + String(httpResponseCode));
  }
  
  http.end();
}

void sendHeartbeat() {
  // Send a safe status heartbeat to keep the system alive
  Serial.println("Sending heartbeat...");
  
  // Use current location (you can modify this to use GPS)
  float defaultLat = 18.52;  // Pune, India
  float defaultLon = 73.85;
  
  sendAlertToServer(false, defaultLat, defaultLon);
}

/*
 * Test function to simulate LoRa data reception
 * Call this function to test the system without actual LoRa hardware
 */
void simulateLoRaData() {
  // Simulate danger alert
  Serial.println("Simulating danger alert...");
  processLoRaData("1,18.5204,73.8567");
  
  delay(5000);
  
  // Simulate safe status
  Serial.println("Simulating safe status...");
  processLoRaData("0,18.5204,73.8567");
}

/*
 * Setup Instructions:
 * 
 * 1. Install required libraries:
 *    - ArduinoJson (by Benoit Blanchon)
 *    - LoRa (by Sandeep Mistry)
 * 
 * 2. Update configuration:
 *    - Change WiFi credentials (ssid, password)
 *    - Update server URL with your backend IP address
 *    - Modify device ID if needed
 * 
 * 3. Hardware connections:
 *    - Connect LoRa module to ESP32:
 *      VCC -> 3.3V
 *      GND -> GND
 *      SCK -> GPIO 18
 *      MISO -> GPIO 19
 *      MOSI -> GPIO 23
 *      CS -> GPIO 5
 *      RST -> GPIO 14
 *      DIO0 -> GPIO 2
 * 
 *    - Connect LEDs (optional):
 *      WiFi LED -> GPIO 12
 *      Danger LED -> GPIO 13
 *      Safe LED -> GPIO 15
 * 
 * 4. Testing:
 *    - Upload code to ESP32
 *    - Open Serial Monitor (115200 baud)
 *    - Check WiFi connection and LoRa initialization
 *    - Send LoRa data in format: "danger,lat,lon"
 *    - Monitor server logs for received data
 * 
 * 5. LoRa Sender (separate device):
 *    Send data in format: "1,18.5204,73.8567" for danger
 *    Send data in format: "0,18.5204,73.8567" for safe
 */