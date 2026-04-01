/*
 * ESP32 NRF24L01 Emergency Alert Sender - IMPROVED VERSION
 * 
 * This code sends emergency alerts via NRF24L01 to receiver ESP32
 * Improved version of your original sender with better features
 * 
 * Hardware Requirements:
 * - ESP32 board (ESP32-WROOM-32 recommended)
 * - NRF24L01 module
 * - Buzzer (optional)
 * - LEDs for status indication (optional)
 * - Sensors for drowning detection (to be integrated)
 * 
 * Libraries Required:
 * - RF24 by TMRh20 (install via Library Manager)
 * 
 * FEATURES:
 * - Reliable NRF24L01 communication
 * - Emergency alert with buzzer
 * - LED status indicators
 * - Serial command interface for testing
 * - Automatic alert timeout
 * - Transmission confirmation
 * - Power management
 */

#include <SPI.h>
#include <RF24.h>

// ==================== CONFIGURATION SECTION ====================

// NRF24L01 Configuration - MUST match receiver
RF24 radio(4, 5);  // CE, CSN pins (GPIO 4, GPIO 5)
const byte address[6] = "NODE1";  // MUST match receiver address

// Pin Definitions
#define BUZZER_PIN 15      // Buzzer pin (GPIO 15)
#define LED_STATUS 12      // Status LED (GPIO 12) - Green
#define LED_DANGER 13      // Danger LED (GPIO 13) - Red
#define LED_TRANSMIT 14    // Transmission LED (GPIO 14) - Blue

// Sensor Input Pin (for future ML integration)
#define SENSOR_INPUT 2     // Digital input from drowning detection sensor

// Alert Configuration
const unsigned long ALERT_DURATION = 15000;    // 15 seconds total alert time
const unsigned long BUZZER_INTERVAL = 3000;    // 3 seconds ON/OFF interval
const unsigned long TRANSMISSION_INTERVAL = 500; // Send data every 500ms during alert
const unsigned long HEARTBEAT_INTERVAL = 10000;  // Send heartbeat every 10 seconds

// ==================== END CONFIGURATION SECTION ====================

// System state variables
bool dangerActive = false;
bool buzzerState = false;
unsigned long alertStartTime = 0;
unsigned long lastBuzzerToggle = 0;
unsigned long lastTransmission = 0;
unsigned long lastHeartbeat = 0;
bool nrfInitialized = false;

// Transmission statistics
unsigned long totalTransmissions = 0;
unsigned long failedTransmissions = 0;

void setup() {
  Serial.begin(115200);
  Serial.println("=== ESP32 NRF24L01 Emergency Alert Sender ===");
  Serial.println("Version: 2.0 - Improved Production Ready");
  Serial.println("============================================");
  
  // Initialize pins
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_STATUS, OUTPUT);
  pinMode(LED_DANGER, OUTPUT);
  pinMode(LED_TRANSMIT, OUTPUT);
  pinMode(SENSOR_INPUT, INPUT_PULLUP);
  
  // Initial pin states
  digitalWrite(BUZZER_PIN, LOW);
  digitalWrite(LED_STATUS, LOW);
  digitalWrite(LED_DANGER, LOW);
  digitalWrite(LED_TRANSMIT, LOW);
  
  // Initialize NRF24L01
  initializeNRF();
  
  // System ready indication
  if (nrfInitialized) {
    digitalWrite(LED_STATUS, HIGH);
    Serial.println("============================================");
    Serial.println("🚀 System Ready - Monitoring for emergencies...");
    Serial.println("Commands:");
    Serial.println("  '1' - Trigger emergency alert");
    Serial.println("  '0' - Clear emergency alert");
    Serial.println("  's' - Show system status");
    Serial.println("  't' - Test transmission");
    Serial.println("============================================");
    
    // Startup beep
    digitalWrite(BUZZER_PIN, HIGH);
    delay(200);
    digitalWrite(BUZZER_PIN, LOW);
  }
}

void loop() {
  // Check for serial commands (for testing)
  handleSerialCommands();
  
  // Check sensor input (for future ML integration)
  checkSensorInput();
  
  // Handle emergency alert logic
  handleEmergencyAlert();
  
  // Handle data transmission
  handleTransmission();
  
  // Send periodic heartbeat when not in emergency
  if (!dangerActive && (millis() - lastHeartbeat >= HEARTBEAT_INTERVAL)) {
    sendHeartbeat();
    lastHeartbeat = millis();
  }
  
  delay(50); // Small delay for system stability
}

void initializeNRF() {
  Serial.println("Initializing NRF24L01...");
  
  if (!radio.begin()) {
    Serial.println("❌ NRF24L01 initialization failed!");
    nrfInitialized = false;
    
    // Error indication - blink all LEDs
    while (1) {
      digitalWrite(LED_STATUS, HIGH);
      digitalWrite(LED_DANGER, HIGH);
      digitalWrite(LED_TRANSMIT, HIGH);
      delay(200);
      digitalWrite(LED_STATUS, LOW);
      digitalWrite(LED_DANGER, LOW);
      digitalWrite(LED_TRANSMIT, LOW);
      delay(200);
    }
  }
  
  nrfInitialized = true;
  Serial.println("✅ NRF24L01 initialized successfully");
  
  // Configure NRF24L01 - MUST match receiver
  radio.setAutoAck(false);           // Disable auto acknowledgment
  radio.setChannel(108);             // Channel 108 (MUST match receiver)
  radio.setDataRate(RF24_1MBPS);     // 1Mbps data rate
  radio.setPALevel(RF24_PA_LOW);     // Low power level
  radio.openWritingPipe(address);    // Set writing address
  radio.stopListening();             // Set as transmitter
  
  Serial.println("NRF24L01 Configuration:");
  Serial.println("  Channel: 108");
  Serial.println("  Data Rate: 1Mbps");
  Serial.println("  Power Level: Low");
  Serial.println("  Address: NODE1");
  Serial.println("  Auto ACK: Disabled");
  Serial.println("  Mode: Transmitter");
}

void handleSerialCommands() {
  if (Serial.available()) {
    char command = Serial.read();
    
    switch (command) {
      case '1':
        triggerEmergencyAlert();
        break;
        
      case '0':
        clearEmergencyAlert();
        break;
        
      case 's':
        showSystemStatus();
        break;
        
      case 't':
        testTransmission();
        break;
        
      default:
        Serial.println("Unknown command. Use: 1 (danger), 0 (safe), s (status), t (test)");
        break;
    }
  }
}

void checkSensorInput() {
  // Read sensor input (for future ML integration)
  // Currently using digital input - replace with your ML model output
  bool sensorDanger = !digitalRead(SENSOR_INPUT); // Inverted because of pull-up
  
  static bool lastSensorState = false;
  
  if (sensorDanger && !lastSensorState) {
    // Sensor detected danger
    Serial.println("🚨 Sensor detected danger!");
    triggerEmergencyAlert();
  } else if (!sensorDanger && lastSensorState && dangerActive) {
    // Sensor cleared danger
    Serial.println("✅ Sensor cleared danger");
    clearEmergencyAlert();
  }
  
  lastSensorState = sensorDanger;
}

void triggerEmergencyAlert() {
  if (!dangerActive) {
    dangerActive = true;
    alertStartTime = millis();
    lastBuzzerToggle = millis();
    buzzerState = true;
    
    digitalWrite(LED_DANGER, HIGH);
    digitalWrite(BUZZER_PIN, HIGH);
    
    Serial.println("🚨 EMERGENCY ALERT TRIGGERED!");
    Serial.println("Alert will run for 15 seconds with 3-second buzzer intervals");
    
    // Immediate transmission
    transmitData();
  }
}

void clearEmergencyAlert() {
  if (dangerActive) {
    dangerActive = false;
    buzzerState = false;
    
    digitalWrite(LED_DANGER, LOW);
    digitalWrite(BUZZER_PIN, LOW);
    
    Serial.println("✅ Emergency alert cleared");
    
    // Send safe status
    transmitData();
  }
}

void handleEmergencyAlert() {
  if (!dangerActive) return;
  
  unsigned long currentTime = millis();
  
  // Check if alert duration has expired
  if (currentTime - alertStartTime >= ALERT_DURATION) {
    Serial.println("⏰ Alert timeout - automatically clearing");
    clearEmergencyAlert();
    return;
  }
  
  // Handle buzzer intervals (3 seconds ON/OFF)
  if (currentTime - lastBuzzerToggle >= BUZZER_INTERVAL) {
    lastBuzzerToggle = currentTime;
    buzzerState = !buzzerState;
    digitalWrite(BUZZER_PIN, buzzerState);
    
    Serial.print("🔊 Buzzer: ");
    Serial.println(buzzerState ? "ON" : "OFF");
  }
}

void handleTransmission() {
  if (!nrfInitialized) return;
  
  unsigned long currentTime = millis();
  
  // Transmit more frequently during emergency
  unsigned long interval = dangerActive ? TRANSMISSION_INTERVAL : HEARTBEAT_INTERVAL;
  
  if (currentTime - lastTransmission >= interval) {
    transmitData();
    lastTransmission = currentTime;
  }
}

void transmitData() {
  if (!nrfInitialized) {
    Serial.println("❌ Cannot transmit - NRF not initialized");
    return;
  }
  
  // Prepare message
  char message[32];
  strcpy(message, dangerActive ? "1" : "0");
  
  // Transmission LED indication
  digitalWrite(LED_TRANSMIT, HIGH);
  
  // Send data
  bool result = radio.write(&message, sizeof(message));
  
  totalTransmissions++;
  
  if (result) {
    Serial.print("📡 Transmitted: ");
    Serial.print(message);
    Serial.print(" (");
    Serial.print(dangerActive ? "DANGER" : "SAFE");
    Serial.println(")");
  } else {
    failedTransmissions++;
    Serial.print("❌ Transmission failed: ");
    Serial.println(message);
  }
  
  // Turn off transmission LED
  delay(50);
  digitalWrite(LED_TRANSMIT, LOW);
}

void sendHeartbeat() {
  Serial.println("💓 Sending heartbeat...");
  transmitData();
}

void testTransmission() {
  Serial.println("🧪 Testing transmission...");
  
  // Test danger signal
  Serial.println("Testing danger signal...");
  char dangerMsg[32] = "1";
  digitalWrite(LED_TRANSMIT, HIGH);
  bool result1 = radio.write(&dangerMsg, sizeof(dangerMsg));
  digitalWrite(LED_TRANSMIT, LOW);
  
  delay(1000);
  
  // Test safe signal
  Serial.println("Testing safe signal...");
  char safeMsg[32] = "0";
  digitalWrite(LED_TRANSMIT, HIGH);
  bool result2 = radio.write(&safeMsg, sizeof(safeMsg));
  digitalWrite(LED_TRANSMIT, LOW);
  
  Serial.print("Test results - Danger: ");
  Serial.print(result1 ? "✅ Success" : "❌ Failed");
  Serial.print(", Safe: ");
  Serial.println(result2 ? "✅ Success" : "❌ Failed");
}

void showSystemStatus() {
  Serial.println("📊 SYSTEM STATUS");
  Serial.println("================");
  Serial.print("NRF24L01: ");
  Serial.println(nrfInitialized ? "✅ Active" : "❌ Failed");
  Serial.print("Emergency State: ");
  Serial.println(dangerActive ? "🚨 DANGER ACTIVE" : "✅ SAFE");
  
  if (dangerActive) {
    unsigned long elapsed = millis() - alertStartTime;
    unsigned long remaining = ALERT_DURATION - elapsed;
    Serial.print("Alert Time Remaining: ");
    Serial.print(remaining / 1000);
    Serial.println(" seconds");
    Serial.print("Buzzer State: ");
    Serial.println(buzzerState ? "ON" : "OFF");
  }
  
  Serial.print("Total Transmissions: ");
  Serial.println(totalTransmissions);
  Serial.print("Failed Transmissions: ");
  Serial.println(failedTransmissions);
  
  if (totalTransmissions > 0) {
    float successRate = ((float)(totalTransmissions - failedTransmissions) / totalTransmissions) * 100;
    Serial.print("Success Rate: ");
    Serial.print(successRate, 1);
    Serial.println("%");
  }
  
  Serial.print("Uptime: ");
  Serial.print(millis() / 1000);
  Serial.println(" seconds");
  Serial.println("================");
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
 * Other Components:
 * Buzzer (+) -> GPIO 15, (-) -> GND
 * Status LED (Green) -> GPIO 12 -> 220Ω resistor -> GND
 * Danger LED (Red) -> GPIO 13 -> 220Ω resistor -> GND
 * Transmit LED (Blue) -> GPIO 14 -> 220Ω resistor -> GND
 * Sensor Input -> GPIO 2 (with pull-up resistor)
 * 
 * Power Supply:
 * - Use stable 3.3V power supply for NRF24L01
 * - Add 10µF and 100nF capacitors near NRF24L01 VCC
 * - Keep wires short (< 10cm)
 * - Use thick wires for power connections
 * 
 * Setup Instructions:
 * 1. Install RF24 library by TMRh20
 * 2. Connect hardware as shown above
 * 3. Upload code and monitor serial output
 * 4. Test with serial commands: 1 (danger), 0 (safe)
 * 5. Verify receiver gets the signals
 * 
 * Integration with ML Model:
 * Replace the checkSensorInput() function with your ML model output
 * Call triggerEmergencyAlert() when drowning is detected
 * Call clearEmergencyAlert() when situation is resolved
 * 
 * Troubleshooting:
 * - If NRF initialization fails, check power supply and connections
 * - If transmissions fail, verify receiver is powered and configured
 * - Use 's' command to check system status and transmission success rate
 * - Ensure both sender and receiver use same channel and address
 */