/*
 * ESP32 Simple Alert Receiver
 * Basic receiver with LoRa + NRF + Buzzer for emergency alerts
 */

#include <SPI.h>
#include <RF24.h>
#include <LoRa.h>

// Pins
#define NRF_CE_PIN 4
#define NRF_CSN_PIN 5
#define LORA_SS_PIN 18
#define LORA_RST_PIN 14
#define LORA_DIO0_PIN 26
#define BUZZER_PIN 25
#define LED_PIN 2
#define BUTTON_PIN 0

// Modules
RF24 radio(NRF_CE_PIN, NRF_CSN_PIN);

// Config
const byte nrfAddress[6] = "00001";
const long loraFreq = 433E6;

// Data structure
struct EmergencyData {
  uint32_t deviceId;
  float lat, lon;
  bool emergency;
  bool button;
  uint8_t battery;
  uint32_t timestamp;
};

EmergencyData data;
bool alertActive = false;
unsigned long alertTime = 0;

void setup() {
  Serial.begin(115200);
  
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  // Init NRF24L01
  radio.begin();
  radio.openReadingPipe(0, nrfAddress);
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(76);
  radio.startListening();
  
  // Init LoRa
  LoRa.setPins(LORA_SS_PIN, LORA_RST_PIN, LORA_DIO0_PIN);
  LoRa.begin(loraFreq);
  LoRa.setSpreadingFactor(12);
  
  Serial.println("Alert Receiver Ready");
  
  // Startup beep
  digitalWrite(BUZZER_PIN, HIGH);
  delay(200);
  digitalWrite(BUZZER_PIN, LOW);
}

void loop() {
  // Check button
  if (digitalRead(BUTTON_PIN) == LOW) {
    alertActive = false;
    digitalWrite(LED_PIN, LOW);
    Serial.println("Alert silenced");
    delay(500);
  }
  
  // Check NRF24L01
  if (radio.available()) {
    radio.read(&data, sizeof(data));
    Serial.println("NRF24 data received");
    processAlert();
  }
  
  // Check LoRa
  int packetSize = LoRa.parsePacket();
  if (packetSize == sizeof(EmergencyData)) {
    LoRa.readBytes((uint8_t*)&data, sizeof(data));
    Serial.println("LoRa data received");
    processAlert();
  }
  
  // Handle active alert
  if (alertActive) {
    handleAlert();
  }
  
  delay(10);
}

void processAlert() {
  Serial.print("Device: 0x"); Serial.println(data.deviceId, HEX);
  Serial.print("Location: "); Serial.print(data.lat, 6);
  Serial.print(", "); Serial.println(data.lon, 6);
  Serial.print("Emergency: "); Serial.println(data.emergency ? "YES" : "NO");
  Serial.print("Button: "); Serial.println(data.button ? "PRESSED" : "NO");
  Serial.print("Battery: "); Serial.print(data.battery); Serial.println("%");
  
  if (data.emergency || data.button) {
    triggerAlert();
  }
}

void triggerAlert() {
  alertActive = true;
  alertTime = millis();
  
  Serial.println("🚨 EMERGENCY ALERT! 🚨");
  
  // Immediate alert
  for (int i = 0; i < 10; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    digitalWrite(LED_PIN, HIGH);
    delay(100);
    digitalWrite(BUZZER_PIN, LOW);
    digitalWrite(LED_PIN, LOW);
    delay(100);
  }
}

void handleAlert() {
  // Flash LED
  digitalWrite(LED_PIN, (millis() / 500) % 2);
  
  // Buzzer every 3 seconds
  if ((millis() - alertTime) % 3000 < 100) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(200);
    digitalWrite(BUZZER_PIN, LOW);
  }
  
  // Auto-reset after 5 minutes
  if (millis() - alertTime > 300000) {
    alertActive = false;
    digitalWrite(LED_PIN, LOW);
    Serial.println("Alert auto-reset");
  }
}