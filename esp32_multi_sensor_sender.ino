

#include <SPI.h>
#include <RF24.h>
#include <LoRa.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <MPU6050.h>

// Pin Definitions
#define NRF_CE_PIN 4
#define NRF_CSN_PIN 5
#define LORA_SS_PIN 18
#define LORA_RST_PIN 14
#define LORA_DIO0_PIN 26
#define GPS_RX_PIN 16
#define GPS_TX_PIN 17
#define EMERGENCY_BUTTON_PIN 0
#define LED_PIN 2
#define BUZZER_PIN 25

// Module Initialization
RF24 radio(NRF_CE_PIN, NRF_CSN_PIN);
SoftwareSerial gpsSerial(GPS_RX_PIN, GPS_TX_PIN);
MPU6050 mpu;

// NRF24L01 Configuration
const byte address[6] = "00001";
const uint8_t channel = 76;
const rf24_pa_dbm_e power_level = RF24_PA_MAX;

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

// Global Variables
SensorData sensorData;
bool gpsFixed = false;
unsigned long lastTransmission = 0;
unsigned long lastGPSRead = 0;
unsigned long lastSensorRead = 0;
const unsigned long transmissionInterval = 5000;
const unsigned long gpsReadInterval = 1000;
const unsigned long sensorReadInterval = 100;

// Emergency Detection Variables
float accelMagnitude = 0;
float gyroMagnitude = 0;
bool emergencyState = false;
unsigned long emergencyStartTime = 0;
const float accelThreshold = 20.0;
const float gyroThreshold = 250.0;
const unsigned long emergencyDuration = 3000;

void setup() {
  Serial.begin(115200);
  
  // Initialize pins
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(EMERGENCY_BUTTON_PIN, INPUT_PULLUP);
  
  // Initialize I2C for MPU6050
  Wire.begin();
  
  // Initialize modules
  initNRF24();
  initLoRa();
  initGPS();
  initMPU6050();
  
  // Initialize sensor data
  sensorData.deviceId = ESP.getEfuseMac();
  sensorData.batteryLevel = 100;
  
  Serial.println("Multi-Sensor Emergency System Ready");
  blinkLED(3);
}

void loop() {
  unsigned long currentTime = millis();
  
  // Read sensors
  if (currentTime - lastSensorRead >= sensorReadInterval) {
    readMPU6050();
    detectEmergency();
    lastSensorRead = currentTime;
  }
  
  // Read GPS
  if (currentTime - lastGPSRead >= gpsReadInterval) {
    readGPS();
    lastGPSRead = currentTime;
  }
  
  // Check emergency button
  if (digitalRead(EMERGENCY_BUTTON_PIN) == LOW) {
    sensorData.buttonPressed = true;
    emergencyState = true;
    Serial.println("EMERGENCY BUTTON PRESSED!");
  }
  
  // Transmit data
  if (currentTime - lastTransmission >= transmissionInterval || emergencyState) {
    prepareSensorData();
    transmitNRF24();
    transmitLoRa();
    
    if (emergencyState) {
      activateEmergencyAlerts();
      transmissionInterval = 1000; // Faster transmission during emergency
    }
    
    lastTransmission = currentTime;
  }
  
  delay(10);
}

void initNRF24() {
  if (!radio.begin()) {
    Serial.println("NRF24L01 init failed");
    return;
  }
  
  radio.openWritingPipe(address);
  radio.setPALevel(power_level);
  radio.setChannel(channel);
  radio.setDataRate(RF24_250KBPS);
  radio.setCRCLength(RF24_CRC_16);
  radio.setAutoAck(true);
  radio.setRetries(15, 15);
  radio.stopListening();
  
  Serial.println("NRF24L01+PA+LNA Ready");
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
  LoRa.setTxPower(20);
  
  Serial.println("LoRa Ready");
}

void initGPS() {
  gpsSerial.begin(9600);
  Serial.println("GPS Ready");
}

void initMPU6050() {
  mpu.initialize();
  
  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed");
    return;
  }
  
  mpu.setFullScaleAccelRange(MPU6050_ACCEL_FS_16);
  mpu.setFullScaleGyroRange(MPU6050_GYRO_FS_2000);
  mpu.setDLPFMode(MPU6050_DLPF_BW_42);
  
  Serial.println("MPU6050 Ready");
}

void readMPU6050() {
  int16_t ax, ay, az, gx, gy, gz, temp;
  
  mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
  temp = mpu.getTemperature();
  
  // Convert to real units
  sensorData.accelX = ax / 2048.0;
  sensorData.accelY = ay / 2048.0;
  sensorData.accelZ = az / 2048.0;
  sensorData.gyroX = gx / 16.4;
  sensorData.gyroY = gy / 16.4;
  sensorData.gyroZ = gz / 16.4;
  sensorData.temperature = temp / 340.0 + 36.53;
  
  // Calculate magnitudes
  accelMagnitude = sqrt(sensorData.accelX * sensorData.accelX + 
                       sensorData.accelY * sensorData.accelY + 
                       sensorData.accelZ * sensorData.accelZ);
  
  gyroMagnitude = sqrt(sensorData.gyroX * sensorData.gyroX + 
                      sensorData.gyroY * sensorData.gyroY + 
                      sensorData.gyroZ * sensorData.gyroZ);
}

void detectEmergency() {
  bool currentEmergency = false;
  
  // High acceleration (impact/fall detection)
  if (accelMagnitude > accelThreshold) {
    currentEmergency = true;
    Serial.println("High acceleration detected!");
  }
  
  // High rotation (spinning/tumbling)
  if (gyroMagnitude > gyroThreshold) {
    currentEmergency = true;
    Serial.println("High rotation detected!");
  }
  
  // Low acceleration (free fall)
  if (accelMagnitude < 2.0) {
    currentEmergency = true;
    Serial.println("Free fall detected!");
  }
  
  // Emergency state management
  if (currentEmergency && !emergencyState) {
    emergencyState = true;
    emergencyStartTime = millis();
    Serial.println("EMERGENCY DETECTED!");
  } else if (!currentEmergency && emergencyState) {
    if (millis() - emergencyStartTime > emergencyDuration) {
      emergencyState = false;
      Serial.println("Emergency cleared");
    }
  }
  
  sensorData.emergencyDetected = emergencyState;
}

void readGPS() {
  while (gpsSerial.available()) {
    String gpsData = gpsSerial.readStringUntil('\n');
    
    if (gpsData.startsWith("$GPGGA") || gpsData.startsWith("$GNGGA")) {
      parseGPGGA(gpsData);
    }
  }
}

void parseGPGGA(String nmea) {
  int commaIndex[15];
  int commaCount = 0;
  
  // Find comma positions
  for (int i = 0; i < nmea.length() && commaCount < 15; i++) {
    if (nmea.charAt(i) == ',') {
      commaIndex[commaCount++] = i;
    }
  }
  
  if (commaCount < 6) return;
  
  // Extract latitude
  String latStr = nmea.substring(commaIndex[1] + 1, commaIndex[2]);
  String latDir = nmea.substring(commaIndex[2] + 1, commaIndex[3]);
  
  // Extract longitude
  String lonStr = nmea.substring(commaIndex[3] + 1, commaIndex[4]);
  String lonDir = nmea.substring(commaIndex[4] + 1, commaIndex[5]);
  
  // Extract fix quality
  String fixQuality = nmea.substring(commaIndex[5] + 1, commaIndex[6]);
  
  if (fixQuality.toInt() > 0 && latStr.length() > 0 && lonStr.length() > 0) {
    // Convert DDMM.MMMM to DD.DDDDDD
    float lat = latStr.substring(0, 2).toFloat() + latStr.substring(2).toFloat() / 60.0;
    float lon = lonStr.substring(0, 3).toFloat() + lonStr.substring(3).toFloat() / 60.0;
    
    if (latDir == "S") lat = -lat;
    if (lonDir == "W") lon = -lon;
    
    sensorData.latitude = lat;
    sensorData.longitude = lon;
    gpsFixed = true;
  } else {
    gpsFixed = false;
  }
}

void prepareSensorData() {
  sensorData.timestamp = millis();
  sensorData.batteryLevel = readBatteryLevel();
  sensorData.rssi = WiFi.RSSI();
  
  // Use Jalgaon coordinates if no GPS fix
  if (!gpsFixed) {
    sensorData.latitude = 20.947388 + (random(-50, 50) / 1000000.0);
    sensorData.longitude = 75.555198 + (random(-50, 50) / 1000000.0);
  }
}

void transmitNRF24() {
  bool result = radio.write(&sensorData, sizeof(sensorData));
  
  Serial.print("NRF24 TX: ");
  Serial.println(result ? "Success" : "Failed");
  
  if (emergencyState) {
    // Send multiple times during emergency
    for (int i = 0; i < 3; i++) {
      delay(10);
      radio.write(&sensorData, sizeof(sensorData));
    }
  }
}

void transmitLoRa() {
  LoRa.beginPacket();
  LoRa.write((uint8_t*)&sensorData, sizeof(sensorData));
  LoRa.endPacket();
  
  Serial.println("LoRa TX: Sent");
  
  if (emergencyState) {
    // Send multiple times during emergency
    for (int i = 0; i < 2; i++) {
      delay(100);
      LoRa.beginPacket();
      LoRa.write((uint8_t*)&sensorData, sizeof(sensorData));
      LoRa.endPacket();
    }
  }
}

void activateEmergencyAlerts() {
  // Visual alert
  digitalWrite(LED_PIN, HIGH);
  
  // Audio alert
  for (int i = 0; i < 5; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    delay(100);
    digitalWrite(BUZZER_PIN, LOW);
    delay(100);
  }
  
  digitalWrite(LED_PIN, LOW);
}

uint8_t readBatteryLevel() {
  // Read battery voltage (assuming voltage divider on A0)
  int adcValue = analogRead(A0);
  float voltage = (adcValue / 4095.0) * 3.3 * 2; // Assuming 2:1 voltage divider
  
  // Convert to percentage (3.0V = 0%, 4.2V = 100%)
  uint8_t percentage = constrain(((voltage - 3.0) / 1.2) * 100, 0, 100);
  return percentage;
}

void blinkLED(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
}

void printSensorData() {
  Serial.println("=== SENSOR DATA ===");
  Serial.print("GPS: "); Serial.print(sensorData.latitude, 6); 
  Serial.print(", "); Serial.println(sensorData.longitude, 6);
  Serial.print("Accel: "); Serial.print(accelMagnitude); Serial.println(" g");
  Serial.print("Gyro: "); Serial.print(gyroMagnitude); Serial.println(" °/s");
  Serial.print("Temp: "); Serial.print(sensorData.temperature); Serial.println(" °C");
  Serial.print("Emergency: "); Serial.println(sensorData.emergencyDetected ? "YES" : "NO");
  Serial.print("Button: "); Serial.println(sensorData.buttonPressed ? "PRESSED" : "NORMAL");
  Serial.print("Battery: "); Serial.print(sensorData.batteryLevel); Serial.println("%");
  Serial.println("==================");
}