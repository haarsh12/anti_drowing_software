#include <esp_now.h>
#include <WiFi.h>
#include <SoftwareSerial.h>
#include <Wire.h>
#include <MPU6050.h>

uint8_t receiverMAC[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

#define GPS_RX_PIN 16
#define GPS_TX_PIN 17
#define EMERGENCY_BUTTON_PIN 0
#define LED_PIN 2
#define BUZZER_PIN 25

SoftwareSerial gpsSerial(GPS_RX_PIN, GPS_TX_PIN);
MPU6050 mpu;

typedef struct struct_message {
  int id;
  float lat;
  float lon;
} struct_message;

struct_message myData;

bool gpsFixed = false;
bool emergencyDetected = false;
unsigned long lastTransmission = 0;
const unsigned long transmissionInterval = 5000;
int messageID = 1;

float accelMagnitude = 0;
const float accelThreshold = 20.0;

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("Send Status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Success" : "Failed");
}

void setup() {
  Serial.begin(115200);
  
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(EMERGENCY_BUTTON_PIN, INPUT_PULLUP);
  
  Wire.begin();
  gpsSerial.begin(9600);
  
  WiFi.mode(WIFI_STA);
  
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW Init Failed");
    return;
  }
  
  esp_now_register_send_cb(OnDataSent);
  
  esp_now_peer_info_t peerInfo;
  memcpy(peerInfo.peer_addr, receiverMAC, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;
  
  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add peer");
    return;
  }
  
  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("MPU6050 connection failed");
  }
  
  myData.lat = 20.947388;
  myData.lon = 75.555198;
  
  Serial.println("ESP-NOW Sender Ready");
  digitalWrite(LED_PIN, HIGH);
  delay(500);
  digitalWrite(LED_PIN, LOW);
}

void loop() {
  unsigned long currentTime = millis();
  
  readMPU6050();
  readGPS();
  checkEmergencyButton();
  detectEmergency();
  
  if (currentTime - lastTransmission >= transmissionInterval || emergencyDetected) {
    prepareData();
    sendData();
    lastTransmission = currentTime;
    
    if (emergencyDetected) {
      activateEmergencyAlerts();
    }
  }
  
  delay(100);
}

void readMPU6050() {
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);
  
  float accelX = ax / 16384.0;
  float accelY = ay / 16384.0;
  float accelZ = az / 16384.0;
  
  accelMagnitude = sqrt(accelX * accelX + accelY * accelY + accelZ * accelZ);
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
  
  for (int i = 0; i < nmea.length() && commaCount < 15; i++) {
    if (nmea.charAt(i) == ',') {
      commaIndex[commaCount++] = i;
    }
  }
  
  if (commaCount < 6) return;
  
  String latStr = nmea.substring(commaIndex[1] + 1, commaIndex[2]);
  String latDir = nmea.substring(commaIndex[2] + 1, commaIndex[3]);
  String lonStr = nmea.substring(commaIndex[3] + 1, commaIndex[4]);
  String lonDir = nmea.substring(commaIndex[4] + 1, commaIndex[5]);
  String fixQuality = nmea.substring(commaIndex[5] + 1, commaIndex[6]);
  
  if (fixQuality.toInt() > 0 && latStr.length() > 0 && lonStr.length() > 0) {
    float lat = latStr.substring(0, 2).toFloat() + latStr.substring(2).toFloat() / 60.0;
    float lon = lonStr.substring(0, 3).toFloat() + lonStr.substring(3).toFloat() / 60.0;
    
    if (latDir == "S") lat = -lat;
    if (lonDir == "W") lon = -lon;
    
    myData.lat = lat;
    myData.lon = lon;
    gpsFixed = true;
  }
}

void checkEmergencyButton() {
  if (digitalRead(EMERGENCY_BUTTON_PIN) == LOW) {
    emergencyDetected = true;
    Serial.println("EMERGENCY BUTTON PRESSED!");
    delay(1000);
  }
}

void detectEmergency() {
  if (accelMagnitude > accelThreshold) {
    emergencyDetected = true;
    Serial.println("HIGH ACCELERATION DETECTED!");
  }
  
  if (accelMagnitude < 2.0) {
    emergencyDetected = true;
    Serial.println("FREE FALL DETECTED!");
  }
}

void prepareData() {
  myData.id = messageID++;
  
  if (!gpsFixed) {
    myData.lat = 20.947388 + (random(-50, 50) / 1000000.0);
    myData.lon = 75.555198 + (random(-50, 50) / 1000000.0);
  }
}

void sendData() {
  esp_err_t result = esp_now_send(receiverMAC, (uint8_t *) &myData, sizeof(myData));
  
  Serial.print("Sending ID: ");
  Serial.print(myData.id);
  Serial.print(" Lat: ");
  Serial.print(myData.lat, 6);
  Serial.print(" Lon: ");
  Serial.print(myData.lon, 6);
  Serial.print(" Emergency: ");
  Serial.println(emergencyDetected ? "YES" : "NO");
  
  if (result == ESP_OK) {
    digitalWrite(LED_PIN, HIGH);
    delay(100);
    digitalWrite(LED_PIN, LOW);
  }
  
  if (emergencyDetected) {
    for (int i = 0; i < 3; i++) {
      delay(100);
      esp_now_send(receiverMAC, (uint8_t *) &myData, sizeof(myData));
    }
    emergencyDetected = false;
  }
}

void activateEmergencyAlerts() {
  for (int i = 0; i < 5; i++) {
    digitalWrite(BUZZER_PIN, HIGH);
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(BUZZER_PIN, LOW);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
}