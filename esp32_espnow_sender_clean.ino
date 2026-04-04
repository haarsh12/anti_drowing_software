#include <esp_now.h>
#include <WiFi.h>
#include "esp_wifi.h"

uint8_t receiverAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

typedef struct struct_message {
  int id;
  float lat;
  float lon;
} struct_message;

struct_message myData;

#define LED_PIN 2
#define BUTTON_PIN 0

bool buttonPressed = false;
unsigned long lastSend = 0;
const unsigned long sendInterval = 5000;
int messageCount = 0;

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("Send Status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Success" : "Fail");
  
  if (status == ESP_NOW_SEND_SUCCESS) {
    digitalWrite(LED_PIN, HIGH);
    delay(100);
    digitalWrite(LED_PIN, LOW);
  }
}

void setup() {
  Serial.begin(115200);
  
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();
  delay(100);
  
  esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
  
  Serial.print("Sender MAC: ");
  Serial.println(WiFi.macAddress());
  
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW Init Failed");
    return;
  }
  
  esp_now_register_send_cb(OnDataSent);
  
  esp_now_peer_info_t peerInfo;
  memcpy(peerInfo.peer_addr, receiverAddress, 6);
  peerInfo.channel = 1;
  peerInfo.encrypt = false;
  
  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add peer");
    return;
  }
  
  Serial.println("ESP-NOW Sender Ready");
  
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_PIN, HIGH);
    delay(200);
    digitalWrite(LED_PIN, LOW);
    delay(200);
  }
}

void loop() {
  if (digitalRead(BUTTON_PIN) == LOW && !buttonPressed) {
    buttonPressed = true;
    sendEmergencyData();
    delay(500);
  }
  
  if (digitalRead(BUTTON_PIN) == HIGH) {
    buttonPressed = false;
  }
  
  if (millis() - lastSend >= sendInterval) {
    sendPeriodicData();
    lastSend = millis();
  }
  
  delay(10);
}

void sendEmergencyData() {
  messageCount++;
  
  myData.id = messageCount;
  myData.lat = 20.947388 + (random(-50, 50) / 1000000.0);
  myData.lon = 75.555198 + (random(-50, 50) / 1000000.0);
  
  Serial.println("🚨 EMERGENCY BUTTON PRESSED!");
  Serial.print("Sending: ID=");
  Serial.print(myData.id);
  Serial.print(", Lat=");
  Serial.print(myData.lat, 6);
  Serial.print(", Lon=");
  Serial.println(myData.lon, 6);
  
  esp_err_t result = esp_now_send(receiverAddress, (uint8_t *) &myData, sizeof(myData));
  
  if (result == ESP_OK) {
    Serial.println("Emergency sent successfully");
  } else {
    Serial.println("Emergency send failed");
  }
}

void sendPeriodicData() {
  messageCount++;
  
  myData.id = messageCount;
  myData.lat = 20.947388 + (random(-30, 30) / 1000000.0);
  myData.lon = 75.555198 + (random(-30, 30) / 1000000.0);
  
  Serial.print("Periodic send: ID=");
  Serial.print(myData.id);
  Serial.print(", Lat=");
  Serial.print(myData.lat, 6);
  Serial.print(", Lon=");
  Serial.println(myData.lon, 6);
  
  esp_err_t result = esp_now_send(receiverAddress, (uint8_t *) &myData, sizeof(myData));
}