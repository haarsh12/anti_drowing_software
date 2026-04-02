/*
 * ESP32 NRF24L01 Emergency Alert System - MERGED VERSION
 * 
 * This code combines:
 * 1. Working NRF24L01 receiver functionality
 * 2. Backend server connectivity and data transmission
 * 3. Comprehensive error handling and status monitoring
 * 
 * Hardware Requirements:
 * - ESP32 board (ESP32-WROOM-32 recommended)
 * - NRF24L01 module
 * - WiFi connection
 * - LED indicators (optional)
 * 
 * Libraries Required:
 * - WiFi (built-in)
 * - HTTPClient (built-in)
 * - ArduinoJson (install via Library Manager)
 * - RF24 by TMRh20 (install via Library Manager)
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <SPI.h>
#include <RF24.h>

// ==================== CONFIGURATION SECTION ====================
// UPDATE THESE VALUES FOR YOUR SETUP

// WiFi Configuration - CHANGE THESE
const char* ssid = "YOUR_WIFI_SSID";           // Replace with your WiFi network name
const char* password = "YOUR_WIFI_PASSWORD";   // Replace with your WiFi password

// Backend Server Configuration - CHANGE THIS
const char* serverURL = "http://192.168.1.162:8000/api/alert";  // Replace with your server IP
const String deviceID = "ESP32_NRF_RECEIVER_01";   // Unique device identifier

// Location Configuration (if using fixed location)
const double FIXED_LATITUDE = 20.9517;   // Jalgaon coordinates
const double FIXED_LONGITUDE = 75.1681;
const String LOCATION_NAME = "Jalgaon Main Swimming Pool";

// NRF24L01 Configuration - MUST match transmitter
RF24 radio(4, 5);  // CE, CSN pins (GPIO 4, GPIO 5)
const byte address[6] = "NODE1";  // MUST match sender address

// LED pins for status indication (optional)
#define LED_WIFI 12    // WiFi status LED (GPIO 12)
#define LED_DANGER 13  // Danger alert LED (GPIO 13)
#define LED_SAFE 15    // Safe status LED (GPIO 15)

// ==================== END CONFIGURATION SECTION ====================

// Timing variables
unsigned long lastHeartbeat = 0;
const unsigned long heartbeatInterval = 30000; // Send heartbeat every 30 seconds
unsigned long lastStatus = 0;
const unsigned long statusInterval = 1000;     // Status print every 1 second

// Connection status
bool wifiConnected = false;
bool serverReachable = false;
bool nrfInitialized = false;

// Alert management
bool currentDangerState = false;
unsigned long lastDangerAlert = 0;
const unsigned long dangerCooldown = 5000; // 5 seconds between danger alerts

void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("=== ESP32 NRF24L01 Emergency Alert System ===");
  Serial.println("RECEIVER STARTING...");
  Serial.println("Version: 3.0 - Merged NRF + Backend");
  Serial.println("===============================================");
  
  // Initialize LED pins
  pinMode(LED_WIFI, OUTPUT);
  pinMode(LED_DANGER, OUTPUT);
  pinMode(LED_SAFE, OUTPUT);
  
  // Initial LED state - all off except safe
  digitalWrite(LED_WIFI, LOW);
  digitalWrite(LED_DANGER, LOW);
  digitalWrite(LED_SAFE, HIGH); // Safe LED on by default
  
  // Initialize NRF24L01
  Serial.println("Initializing NRF24L01...");
  
  if (!radio.begin()) {
    Serial.println("NRF NOT DETECTED ❌");
    nrfInitialized = false;
    while (1) {
      // Blink all LEDs to indicate NRF error
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
  
  nrfInitialized = true;
  Serial.println("NRF READY ✅");
  
  // Configure NRF24L01 - MUST match transmitter settings
  radio.setAutoAck(false);           // Disable auto acknowledgment
  radio.setChannel(108);             // Channel 108 (MUST match sender)
  radio.setDataRate(RF24_1MBPS);     // 1Mbps data rate
  radio.setPALevel(RF24_PA_LOW);     // Low power level
  radio.openReadingPipe(0, address); // Open reading pipe
  radio.startListening();            // Start listening for data
  radio.flush_rx();                  // Clear any old data
  
  Serial.println("NRF24L01 Configuration:");
  Serial.println("  Channel: 108");
  Serial.println("  Data Rate: 1Mbps");
  Serial.println("  Power Level: Low");
  Serial.println("  Address: NODE1");
  Serial.println("  Auto ACK: Disabled");
  
  // Connect to WiFi
  connectToWiFi();
  
  // Test server connection
  testServerConnection();
  
  Serial.println("===============================================");
  Serial.println("🚀 Receiver Ready - Waiting for data...");
  Serial.println("Expected format: Text messages from NRF sender");
  Serial.println("===============================================");
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
  
  // Check for NRF24L01 data
  if (radio.available()) {
    char text[32] = "";
    radio.read(&text, sizeof(text));
    
    String receivedData = String(text);
    receivedData.trim(); // Remove whitespace
    
    Serial.print("✅ Received: ");
    Serial.println(receivedData);
    
    // Process the received data
    processNRFData(receivedData);
  }
  
  // Status print so you're not blind
  if (millis() - lastStatus > statusInterval) {
    lastStatus = millis();
    Serial.println("⏳ Waiting for data...");
  }
  
  // Send heartbeat
  if (millis() - lastHeartbeat >= heartbeatInterval) {
    lastHeartbeat = millis();
    sendHeartbeat();
  }
  
  // Safety recovery for NRF
  if (!radio.isChipConnected()) {
    Serial.println("⚠️ NRF LOST! Reinitializing...");
    radio.begin();
    radio.setAutoAck(false);
    radio.setChannel(108);
    radio.openReadingPipe(0, address);
    radio.startListening();
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
  DynamicJsonDocument testDoc(300);
  testDoc["device_id"] = deviceID;
  testDoc["danger"] = false;
  testDoc["latitude"] = FIXED_LATITUDE;
  testDoc["longitude"] = FIXED_LONGITUDE;
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
    Serial.println("1. Server IP address in serverURL");
    Serial.println("2. Server is running and accessible");
    Serial.println("3. Firewall settings");
  }
  
  http.end();
}

void processNRFData(String data) {
  bool isDanger = false;
  
  // Parse different data formats
  if (data == "1" || data.equalsIgnoreCase("true") || data.equalsIgnoreCase("danger")) {
    isDanger = true;
  } else if (data == "0" || data.equalsIgnoreCase("false") || data.equalsIgnoreCase("safe")) {
    isDanger = false;
  } else if (data.indexOf("danger") >= 0 || data.indexOf("emergency") >= 0 || data.indexOf("help") >= 0) {
    isDanger = true;
  } else if (data.indexOf("safe") >= 0 || data.indexOf("ok") >= 0 || data.indexOf("normal") >= 0) {
    isDanger = false;
  } else {
    // Default: treat any non-empty message as potential danger
    Serial.println("⚠️ Unknown data format - treating as danger alert");
    isDanger = true;
  }
  
  Serial.println("📊 Parsed data:");
  Serial.print("Danger status: ");
  Serial.println(isDanger ? "🚨 DANGER DETECTED!" : "✅ SAFE");
  Serial.print("Location: ");
  Serial.print(LOCATION_NAME);
  Serial.print(" (");
  Serial.print(FIXED_LATITUDE, 6);
  Serial.print(", ");
  Serial.print(FIXED_LONGITUDE, 6);
  Serial.println(")");
  
  // Update LEDs based on danger status
  if (isDanger) {
    digitalWrite(LED_DANGER, HIGH);
    digitalWrite(LED_SAFE, LOW);
    Serial.println("🚨 EMERGENCY ALERT - Sending to server!");
    
    // Prevent spam alerts - only send if state changed or cooldown passed
    if (!currentDangerState || (millis() - lastDangerAlert > dangerCooldown)) {
      currentDangerState = true;
      lastDangerAlert = millis();
      sendToServer(true, data);
    } else {
      Serial.println("⏳ Danger alert cooldown active - skipping duplicate");
    }
  } else {
    digitalWrite(LED_DANGER, LOW);
    digitalWrite(LED_SAFE, HIGH);
    Serial.println("✅ Safe status received");
    
    // Send safe status if we were previously in danger
    if (currentDangerState) {
      currentDangerState = false;
      sendToServer(false, data);
    }
  }
}

void sendToServer(bool danger, String originalMessage) {
  if (!wifiConnected) {
    Serial.println("❌ Cannot send - WiFi not connected");
    return;
  }
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("User-Agent", "ESP32HTTPClient/1.0");
  
  // Create comprehensive JSON payload
  DynamicJsonDocument doc(600);
  doc["device_id"] = deviceID;
  doc["danger"] = danger;
  doc["latitude"] = FIXED_LATITUDE;
  doc["longitude"] = FIXED_LONGITUDE;
  doc["location_name"] = LOCATION_NAME;
  doc["original_message"] = originalMessage;
  
  // Add system information
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["uptime"] = millis();
  doc["timestamp"] = millis();
  doc["nrf_status"] = nrfInitialized ? "active" : "failed";
  doc["heartbeat"] = false;
  doc["test"] = false;
  doc["free_heap"] = ESP.getFreeHeap();
  doc["chip_id"] = String(ESP.getEfuseMac(), HEX);
  
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
    } else {
      Serial.println("✅ Safe status sent successfully!");
    }
  } else {
    Serial.print("❌ HTTP Error code: ");
    Serial.println(httpResponseCode);
    Serial.println("Possible issues:");
    Serial.println("  • Server not running");
    Serial.println("  • Wrong IP address");
    Serial.println("  • Firewall blocking connection");
    
    serverReachable = false;
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
  http.addHeader("User-Agent", "ESP32HTTPClient/1.0");
  
  // Create heartbeat payload
  DynamicJsonDocument doc(500);
  doc["device_id"] = deviceID;
  doc["danger"] = false;
  doc["latitude"] = FIXED_LATITUDE;
  doc["longitude"] = FIXED_LONGITUDE;
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
  doc["nrf_status"] = nrfInitialized ? "active" : "failed";
  doc["current_state"] = currentDangerState ? "danger" : "safe";
  
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
  Serial.print("NRF24L01: ");
  Serial.println(nrfInitialized ? "✅ Active" : "❌ Failed");
  Serial.print("Current State: ");
  Serial.println(currentDangerState ? "🔴 DANGER" : "🟢 SAFE");
  Serial.print("Uptime: ");
  Serial.print(millis() / 1000);
  Serial.println(" seconds");
  Serial.println("==========================================");
}

/*
 * HARDWARE CONNECTION GUIDE:
 * 
 * NRF24L01 to ESP32:
 * VCC -> 3.3V (IMPORTANT: Use 3.3V, not 5V!)
 * GND -> GND
 * CE  -> GPIO 4
 * CSN -> GPIO 5
 * SCK -> GPIO 18
 * MOSI -> GPIO 23
 * MISO -> GPIO 19
 * IRQ -> Not connected
 * 
 * LEDs (Optional):
 * WiFi LED (Green)   -> GPIO 12 -> 220Ω resistor -> GND
 * Danger LED (Red)   -> GPIO 13 -> 220Ω resistor -> GND
 * Safe LED (Blue)    -> GPIO 15 -> 220Ω resistor -> GND
 * 
 * SETUP INSTRUCTIONS:
 * 1. Install required libraries:
 *    - RF24 by TMRh20
 *    - ArduinoJson by Benoit Blanchon
 * 
 * 2. Update configuration section:
 *    - WiFi credentials (ssid, password)
 *    - Server URL with your backend IP
 *    - Location coordinates if needed
 * 
 * 3. Hardware connections as shown above
 * 
 * 4. Upload code and monitor serial output
 * 
 * 5. Test with your NRF sender device
 * 
 * TROUBLESHOOTING:
 * - If NRF initialization fails: Check power supply and connections
 * - If no data received: Verify sender/receiver use same channel/address
 * - If WiFi fails: Check credentials and signal strength
 * - If server unreachable: Verify IP address and firewall settings
 */