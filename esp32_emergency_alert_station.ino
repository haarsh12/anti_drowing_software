/*
 * ESP32 Emergency Alert Station
 * Standalone receiver with LoRa + NRF24L01 + Buzzer for immediate alerts
 */

#include <SPI.h>
#include <RF24.h>
#include <LoRa.h>

// Pin Definitions
#define NRF_CE_PIN 4
#define NRF_CSN_PIN 5
#define LORA_SS_PIN 18
#define LORA_RST_PIN 14
#define LORA_DIO0_PIN 26
#define BUZZER_PIN 25
#define LED_EMERGENCY_PIN 2
#define LED_NRF_PIN 12
#define LED_LORA_PIN 13
#define LED_POWER_PIN 15
#define SILENCE_BUTTON_PIN 0

// Module Initialization
RF24 radio(NRF_CE_PIN, NRF_CSN_PIN);

// NRF24L01 Configuration
const byte address[6] = "00001";
const uint8_t channel = 76;

// LoRa Configuration
const long loraFreq = 433E6;
const int loraSF = 12;
const long loraBW = 125E3;

// Data Structure
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
bool emergencyActive = false;
bool buzzerSilenced = false;
unsigned long emergencyStartTime = 0;
unsigned long lastBuzzerTime = 0;
unsigned long lastStatusCheck = 0;
int emergencyCount = 0;
int packetsReceived = 0;

// Buzzer patterns
const int EMERGENCY_PATTERN[] = {200, 100, 200, 100, 200, 500}; // Fast beeps
const int WARNING_PATTERN[] = {500, 500}; // Slow beeps
const int CONFIRM_PATTERN[] = {100, 50, 100, 50, 100}; // Quick confirmation

void setup() {
  Serial.begin(115200);
  
  // Initialize pins
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_EMERGENCY_PIN, OUTPUT);
  pinMode(LED_NRF_PIN, OUTPUT);
  pinMode(LED_LORA_PIN, OUTPUT);
  pinMode(LED_POWER_PIN, OUTPUT);
  pinMode(SILENCE_BUTTON_PIN, INPUT_PULLUP);
  
  // Power on indication
  digitalWrite(LED_POWER_PIN, HIGH);
  
  // Initialize modules
  initNRF24();
  initLoRa();
  
  // Startup sequence
  playBuzzerPattern(CONFIRM_PATTERN, 5);
  blinkAllLEDs(3);
  
  Serial.println("Emergency Alert Station Ready");
  Serial.println("Listening for emergency signals...");
}

void loop() {
  // Check silence button
  if (digitalRead(SILENCE_BUTTON_PIN) == LOW) {
    handleSilenceButton();
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
  
  // Handle emergency alerts
  if (emergencyActive && !buzzerSilenced) {
    handleEmergencyAlert();
  }
  
  // Auto-reset emergency after 5 minutes
  if (emergencyActive && (millis() - emergencyStartTime > 300000)) {
    resetEmergencyState();
  }
  
  // Status check every 10 seconds
  if (millis() - lastStatusCheck > 10000) {
    performStatusCheck();
    lastStatusCheck = millis();
  }
  
  delay(10);
}

void initNRF24() {
  if (!radio.begin()) {
    Serial.println("NRF24L01 init failed");
    blinkLED(LED_NRF_PIN, 10); // Error indication
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
    blinkLED(LED_LORA_PIN, 10); // Error indication
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

void receiveNRF24Data() {
  radio.read(&receivedData, sizeof(receivedData));
  packetsReceived++;
  
  Serial.println("\n=== NRF24L01 EMERGENCY DATA ===");
  printEmergencyData("NRF24L01");
  
  // Visual indication
  blinkLED(LED_NRF_PIN, 2);
  
  // Process emergency
  if (receivedData.emergencyDetected || receivedData.buttonPressed) {
    triggerEmergencyAlert("NRF24L01");
  }
}

void receiveLoRaData(int packetSize) {
  if (packetSize == sizeof(SensorData)) {
    LoRa.readBytes((uint8_t*)&receivedData, sizeof(receivedData));
    packetsReceived++;
    
    Serial.println("\n=== LORA EMERGENCY DATA ===");
    Serial.print("RSSI: "); Serial.print(LoRa.packetRssi()); Serial.println(" dBm");
    Serial.print("SNR: "); Serial.print(LoRa.packetSnr()); Serial.println(" dB");
    printEmergencyData("LoRa");
    
    // Visual indication
    blinkLED(LED_LORA_PIN, 2);
    
    // Process emergency
    if (receivedData.emergencyDetected || receivedData.buttonPressed) {
      triggerEmergencyAlert("LoRa");
    }
  }
}

void triggerEmergencyAlert(String protocol) {
  emergencyActive = true;
  buzzerSilenced = false;
  emergencyStartTime = millis();
  emergencyCount++;
  
  Serial.println("\n🚨🚨🚨 EMERGENCY ALERT TRIGGERED 🚨🚨🚨");
  Serial.print("Protocol: "); Serial.println(protocol);
  Serial.print("Device ID: 0x"); Serial.println(receivedData.deviceId, HEX);
  Serial.print("Location: "); Serial.print(receivedData.latitude, 6);
  Serial.print(", "); Serial.println(receivedData.longitude, 6);
  Serial.print("Emergency Type: ");
  
  if (receivedData.buttonPressed) {
    Serial.println("MANUAL BUTTON PRESS");
  } else {
    Serial.println("AUTOMATIC DETECTION");
  }
  
  Serial.print("Battery Level: "); Serial.print(receivedData.batteryLevel); Serial.println("%");
  Serial.println("🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨");
  
  // Immediate alert
  digitalWrite(LED_EMERGENCY_PIN, HIGH);
  playBuzzerPattern(EMERGENCY_PATTERN, 6);
}

void handleEmergencyAlert() {
  unsigned long currentTime = millis();
  
  // Continuous emergency LED
  digitalWrite(LED_EMERGENCY_PIN, HIGH);
  
  // Buzzer every 3 seconds
  if (currentTime - lastBuzzerTime > 3000) {
    playBuzzerPattern(EMERGENCY_PATTERN, 6);
    lastBuzzerTime = currentTime;
    
    // Print reminder
    Serial.println("🚨 EMERGENCY ACTIVE - Press button to silence buzzer");
    Serial.print("Emergency count: "); Serial.println(emergencyCount);
    Serial.print("Time active: "); Serial.print((currentTime - emergencyStartTime) / 1000); Serial.println(" seconds");
  }
}

void handleSilenceButton() {
  delay(50); // Debounce
  
  if (digitalRead(SILENCE_BUTTON_PIN) == LOW) {
    if (emergencyActive && !buzzerSilenced) {
      // Silence buzzer but keep LED active
      buzzerSilenced = true;
      Serial.println("🔇 Buzzer silenced - Emergency LED remains active");
      playBuzzerPattern(CONFIRM_PATTERN, 5);
    } else if (emergencyActive && buzzerSilenced) {
      // Reset emergency completely
      resetEmergencyState();
      Serial.println("✅ Emergency reset - All alerts cleared");
      playBuzzerPattern(CONFIRM_PATTERN, 5);
    } else {
      // Test all systems
      performSystemTest();
    }
    
    // Wait for button release
    while (digitalRead(SILENCE_BUTTON_PIN) == LOW) {
      delay(10);
    }
  }
}

void resetEmergencyState() {
  emergencyActive = false;
  buzzerSilenced = false;
  digitalWrite(LED_EMERGENCY_PIN, LOW);
  Serial.println("Emergency state reset");
}

void performSystemTest() {
  Serial.println("\n=== SYSTEM TEST ===");
  
  // Test LEDs
  Serial.println("Testing LEDs...");
  blinkAllLEDs(2);
  
  // Test buzzer
  Serial.println("Testing buzzer...");
  playBuzzerPattern(WARNING_PATTERN, 2);
  
  // Show status
  Serial.println("System Status:");
  Serial.print("- NRF24L01: "); Serial.println(digitalRead(LED_NRF_PIN) ? "OK" : "ERROR");
  Serial.print("- LoRa: "); Serial.println(digitalRead(LED_LORA_PIN) ? "OK" : "ERROR");
  Serial.print("- Power: "); Serial.println(digitalRead(LED_POWER_PIN) ? "OK" : "ERROR");
  Serial.print("- Packets received: "); Serial.println(packetsReceived);
  Serial.print("- Emergency count: "); Serial.println(emergencyCount);
  Serial.print("- Uptime: "); Serial.print(millis() / 1000); Serial.println(" seconds");
  Serial.println("==================");
}

void performStatusCheck() {
  // Check module status
  bool nrfOK = digitalRead(LED_NRF_PIN);
  bool loraOK = digitalRead(LED_LORA_PIN);
  
  if (!nrfOK || !loraOK) {
    Serial.println("⚠️ Module error detected - attempting restart...");
    
    if (!nrfOK) {
      digitalWrite(LED_NRF_PIN, LOW);
      initNRF24();
    }
    
    if (!loraOK) {
      digitalWrite(LED_LORA_PIN, LOW);
      initLoRa();
    }
  }
  
  // Heartbeat indication
  blinkLED(LED_POWER_PIN, 1);
}

void printEmergencyData(String protocol) {
  Serial.print("Protocol: "); Serial.println(protocol);
  Serial.print("Device ID: 0x"); Serial.println(receivedData.deviceId, HEX);
  Serial.print("GPS: "); Serial.print(receivedData.latitude, 6);
  Serial.print(", "); Serial.println(receivedData.longitude, 6);
  Serial.print("Emergency: "); Serial.println(receivedData.emergencyDetected ? "YES" : "NO");
  Serial.print("Button: "); Serial.println(receivedData.buttonPressed ? "PRESSED" : "NORMAL");
  Serial.print("Battery: "); Serial.print(receivedData.batteryLevel); Serial.println("%");
  Serial.print("Temperature: "); Serial.print(receivedData.temperature); Serial.println("°C");
  Serial.print("Accel Magnitude: ");
  float accelMag = sqrt(receivedData.accelX * receivedData.accelX + 
                       receivedData.accelY * receivedData.accelY + 
                       receivedData.accelZ * receivedData.accelZ);
  Serial.print(accelMag); Serial.println(" g");
  Serial.print("Timestamp: "); Serial.println(receivedData.timestamp);
  Serial.println("===============================");
}

void playBuzzerPattern(const int pattern[], int length) {
  for (int i = 0; i < length; i += 2) {
    if (i + 1 < length) {
      digitalWrite(BUZZER_PIN, HIGH);
      delay(pattern[i]);
      digitalWrite(BUZZER_PIN, LOW);
      delay(pattern[i + 1]);
    }
  }
}

void blinkLED(int pin, int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(pin, LOW);
    delay(100);
    digitalWrite(pin, HIGH);
    delay(100);
  }
}

void blinkAllLEDs(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_NRF_PIN, LOW);
    digitalWrite(LED_LORA_PIN, LOW);
    digitalWrite(LED_EMERGENCY_PIN, LOW);
    digitalWrite(LED_POWER_PIN, LOW);
    delay(200);
    digitalWrite(LED_NRF_PIN, HIGH);
    digitalWrite(LED_LORA_PIN, HIGH);
    digitalWrite(LED_EMERGENCY_PIN, HIGH);
    digitalWrite(LED_POWER_PIN, HIGH);
    delay(200);
  }
  
  // Reset emergency LED
  if (!emergencyActive) {
    digitalWrite(LED_EMERGENCY_PIN, LOW);
  }
}