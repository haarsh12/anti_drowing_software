/*
 * ESP32 LoRa Emergency Alert System
 * 
 * This code receives LoRa data in format: "danger,latitude,longitude"
 * and sends it to the backend server via HTTP POST request
 * 
 * Hardware Requirements:
 * - ESP32 board
 * - LoRa module (SX1276/SX1278)
 * - WiFi connection
 * 
 * Libraries Required:
 * - WiFi (built-in)
 * - HTTPClient (built-in)
 * - ArduinoJson
 * - LoRa (by Sandeep Mistry)
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <LoRa.h>
#include <SPI.h>

// WiFi Configuration
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Backend Server Configuration
const char* serverURL = "http://192.168.1.100:8000/api/alert";  // Replace with your server IP
const String deviceID = "esp32_1";

// LoRa Configuration
#define SS 5      // LoRa chip select pin
#define RST 14    // LoRa reset pin
#define DIO0 2    // LoRa DIO0 pin
#define FREQUENCY 433E6  // LoRa frequency (433MHz)

// LED pins for status indication
#define LED_WIFI 12    // WiFi status LED
#define LED_DANGER 13  // Danger alert LED
#define LED_SAFE 15    // Safe status LED

// Timing variables
unsigned long lastHeartbeat = 0;
const unsigned long heartbeatInterval = 30000; // Send heartbeat every 30 seconds

void setup() {
  Serial.begin(115200);
  Serial.println("ESP32 LoRa Alert System Starting...");
  
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