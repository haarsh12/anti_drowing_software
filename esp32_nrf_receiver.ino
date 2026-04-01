/*
 * ESP32 NRF24L01 Emergency Alert Receiver - PRODUCTION READY
 * 
 * This code receives NRF24L01 data from sender and forwards to backend server
 * Compatible with your sender code using NRF24L01 modules
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
 * 
 * CONFIGURATION INSTRUCTIONS:
 * 1. Update WiFi credentials below
 * 2. Update server URL with your backend IP address
 * 3. Verify NRF24L01 pin connections match your hardware
 * 4. Upload code to ESP32
 * 5. Monitor Serial output for connection status
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

// NRF24L01 Configuration - VERIFY PIN CONNECTIONS
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
unsigned long lastNRFCheck = 0;
const unsigned long nrfCheckInterval = 100;  // Check NRF every 100ms for responsiveness

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
  Serial.println("=== ESP32 NRF24L01 Emergency Alert Receiver ===");
  Serial.println("Version: 2.0 - Production Ready");
  Serial.println("Compatible with NRF24L01 sender modules");
  Serial.println("===============================================");
  
  // Initialize LED pins
  pinMode(LED_WIFI, OUTPUT);
  pinMode(LED_DANGER, OUTPUT);
  pinMode(LED_SAFE, OUTPUT);
  
  // Initial LED state - all off
  digitalWrite(LED_WIFI, LOW);
  digitalWrite(LED_DANGER, LOW);
  digitalWrite(LED_SAFE, HIGH); // Safe LED on by default
  
  // Initialize NRF24L01
  Serial.println("Initializing NRF24L01...");
  
  if (!radio.begin()) {
    Serial.println("❌ NRF24L01 initialization failed!");
    nrfInitialized = false;
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
  
  nrfInitialized = true;
  Serial.println("✅ NRF24L01 initialized successfully");
  
  // Configure NRF24L01 - MUST match sender configuration
  radio.setAutoAck(false);           // Disable auto acknowledgment
  radio.setChannel(108);             // Channel 108 (MUST match sender)
  radio.setDataRate(RF24_1MBPS);     // 1Mbps data rate
  radio.setPALevel(RF24_PA_LOW);     // Low power level
  radio.openReadingPipe(0, address); // Open reading pipe
  radio.startListening();            // Start listening for data
  
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
  Serial.println("🚀 System ready - Listening for NRF data...");
  Serial.println("Expected data: '1' (danger) or '0' (safe)");
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
  }
  
  // Check for NRF24L01 data
  if (millis() - lastNRFCheck >= nrfCheckInterval) {
    lastNRFCheck = millis();
    checkForNRFData();
  }
  
  // Send heartbeat
  if (millis() - lastHeartbeat >= heartbeatInterval) {
    lastHeartbeat = millis();
    sendHeartbeat();
  }
  
  delay(10); // Small delay to prevent watchdog issues
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

void checkForNRFData() {
  if (!nrfInitialized) return;
  
  if (radio.available()) {
    char receivedMessage[32];
    radio.read(&receivedMessage, sizeof(receivedMessage));
    
    String receivedData = String(receivedMessage);
    receivedData.trim(); // Remove any whitespace
    
    Serial.println("📡 NRF24L01 data received!");
    Serial.print("Raw data: '");
    Serial.print(receivedData);
    Serial.println("'");
    
    // Parse and process data
    processNRFData(receivedData);
  }
}

void processNRFData(String data) {
  bool isDanger = false;
  
  // Parse danger status
  if (data == "1" || data.equalsIgnoreCase("true") || data.equalsIgnoreCase("danger")) {
    isDanger = true;
  } else if (data == "0" || data.equalsIgnoreCase("false") || data.equalsIgnoreCase("safe")) {
    isDanger = false;
  } else {
    Serial.println("❌ Invalid data format received!");
    Serial.println("Expected: '1' (danger) or '0' (safe)");
    return;
  }
  
  Serial.println("📊 Parsed data:");
  Serial.print("Danger status: ");
  Serial.println(isDanger ? "🚨 DANGER DETECTED!" : "✅ SAFE");
  
  // Update LEDs based on danger status
  if (isDanger) {
    digitalWrite(LED_DANGER, HIGH);
    digitalWrite(LED_SAFE, LOW);
    Serial.println("🚨 EMERGENCY ALERT - Sending to server!");
    
    // Prevent spam alerts - only send if state changed or cooldown passed
    if (!currentDangerState || (millis() - lastDangerAlert > dangerCooldown)) {
      currentDangerState = true;
      lastDangerAlert = millis();
      sendToServer(true);
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
      sendToServer(false);
    }
  }
}

void sendToServer(bool danger) {
  if (!wifiConnected) {
    Serial.println("❌ Cannot send - WiFi not connected");
    return;
  }
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("User-Agent", "ESP32HTTPClient/1.0");  // Identify as ESP32
  
  // Create comprehensive JSON payload with debug information
  DynamicJsonDocument doc(500);
  doc["device_id"] = deviceID;
  doc["danger"] = danger;
  doc["latitude"] = FIXED_LATITUDE;
  doc["longitude"] = FIXED_LONGITUDE;
  doc["location_name"] = LOCATION_NAME;
  
  // Add debugging information
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["uptime"] = millis();
  doc["timestamp"] = millis();
  doc["nrf_status"] = nrfInitialized ? "active" : "failed";
  doc["heartbeat"] = false;  // This is not a heartbeat
  doc["test"] = false;       // This is not a test
  
  // Add system information
  doc["free_heap"] = ESP.getFreeHeap();
  doc["chip_id"] = String(ESP.getEfuseMac(), HEX);
  doc["sdk_version"] = ESP.getSdkVersion();
  
  String payload;
  serializeJson(doc, payload);
  
  Serial.println("📤 Sending detailed data to server...");
  Serial.print("🌐 URL: ");
  Serial.println(serverURL);
  Serial.print("📊 Payload size: ");
  Serial.print(payload.length());
  Serial.println(" bytes");
  Serial.print("📄 Full payload: ");
  Serial.println(payload);
  
  int httpResponseCode = http.POST(payload);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.print("✅ Server response code: ");
    Serial.println(httpResponseCode);
    Serial.print("📥 Server response: ");
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
    Serial.println("🔧 Possible issues:");
    Serial.println("   • Server not running");
    Serial.println("   • Wrong IP address");
    Serial.println("   • Firewall blocking connection");
    Serial.println("   • Network connectivity issues");
    
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
  
  Serial.println("💓 Sending detailed heartbeat...");
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("User-Agent", "ESP32HTTPClient/1.0");  // Identify as ESP32
  
  // Create comprehensive heartbeat payload
  DynamicJsonDocument doc(600);
  doc["device_id"] = deviceID;
  doc["danger"] = false;
  doc["latitude"] = FIXED_LATITUDE;
  doc["longitude"] = FIXED_LONGITUDE;
  doc["location_name"] = LOCATION_NAME;
  doc["heartbeat"] = true;  // Mark as heartbeat
  
  // Network information
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["wifi_ssid"] = WiFi.SSID();
  doc["local_ip"] = WiFi.localIP().toString();
  
  // System information
  doc["uptime"] = millis();
  doc["timestamp"] = millis();
  doc["free_heap"] = ESP.getFreeHeap();
  doc["chip_id"] = String(ESP.getEfuseMac(), HEX);
  doc["sdk_version"] = ESP.getSdkVersion();
  doc["cpu_freq"] = ESP.getCpuFreqMHz();
  
  // NRF24L01 status
  doc["nrf_status"] = nrfInitialized ? "active" : "failed";
  
  // Current state
  doc["current_state"] = currentDangerState ? "danger" : "safe";
  
  String payload;
  serializeJson(doc, payload);
  
  Serial.print("� Heartbeat payload size: ");
  Serial.print(payload.length());
  Serial.println(" bytes");
  Serial.print("📄 Heartbeat data: ");
  Serial.println(payload);
  
  int httpResponseCode = http.POST(payload);
  
  if (httpResponseCode > 0) {
    serverReachable = true;
    Serial.print("💓 Heartbeat sent successfully (");
    Serial.print(httpResponseCode);
    Serial.println(")");
    
    // Parse response for any server messages
    String response = http.getString();
    if (response.length() > 0) {
      Serial.print("📥 Server response: ");
      Serial.println(response);
    }
  } else {
    serverReachable = false;
    Serial.print("❌ Heartbeat failed (");
    Serial.print(httpResponseCode);
    Serial.println(")");
    Serial.println("🔧 Troubleshooting heartbeat failure:");
    Serial.println("   • Check server is running");
    Serial.println("   • Verify IP address in serverURL");
    Serial.println("   • Test with: curl http://192.168.1.162:8000/health");
  }
  
  http.end();
  
  // Print comprehensive system status
  Serial.println("📊 DETAILED SYSTEM STATUS:");
  Serial.println("=" * 50);
  Serial.print("🌐 WiFi: ");
  Serial.print(wifiConnected ? "✅ Connected" : "❌ Disconnected");
  if (wifiConnected) {
    Serial.print(" (");
    Serial.print(WiFi.RSSI());
    Serial.print(" dBm, ");
    Serial.print(WiFi.SSID());
    Serial.print(")");
  }
  Serial.println();
  
  Serial.print("🖥️  Server: ");
  Serial.println(serverReachable ? "✅ Reachable" : "❌ Unreachable");
  
  Serial.print("📻 NRF24L01: ");
  Serial.println(nrfInitialized ? "✅ Active" : "❌ Failed");
  
  Serial.print("🚨 Current State: ");
  Serial.println(currentDangerState ? "🔴 DANGER" : "🟢 SAFE");
  
  Serial.print("💾 Free Heap: ");
  Serial.print(ESP.getFreeHeap());
  Serial.println(" bytes");
  
  Serial.print("⏱️  Uptime: ");
  Serial.print(millis() / 1000);
  Serial.println(" seconds");
  
  Serial.print("🆔 Chip ID: ");
  Serial.println(String(ESP.getEfuseMac(), HEX));
  
  Serial.println("=" * 50);
}

/*
 * Hardware Connection Guide:
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
 * Power Supply:
 * - Use stable 3.3V power supply
 * - Add 10µF and 100nF capacitors near NRF24L01 VCC
 * - Keep wires short (< 10cm)
 * 
 * Setup Instructions:
 * 1. Install RF24 library by TMRh20
 * 2. Install ArduinoJson library
 * 3. Update WiFi credentials and server URL
 * 4. Connect hardware as shown above
 * 5. Upload code and monitor serial output
 * 6. Test with sender device
 * 
 * Troubleshooting:
 * - If NRF initialization fails, check power supply and connections
 * - If no data received, verify sender and receiver use same channel/address
 * - If WiFi fails, check credentials and signal strength
 * - If server unreachable, verify IP address and firewall settings
 */