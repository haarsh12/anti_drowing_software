// MINIMAL FIX - Add this to your ESP32 OnDataRecv function
// Replace your current OnDataRecv function with this:

void OnDataRecv(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
  memcpy(&incomingData, data, sizeof(incomingData));
  
  Serial.println("\n📩 RECEIVED");
  Serial.print("ID: ");
  Serial.println(incomingData.id);
  Serial.print("Lat: ");
  Serial.println(incomingData.lat, 6);
  Serial.print("Lon: ");
  Serial.println(incomingData.lon, 6);
  
  digitalWrite(LED_PIN, HIGH);
  delay(200);
  digitalWrite(LED_PIN, LOW);
  
  // CRITICAL FIX: Send emergency data immediately
  Serial.println("🚨 SENDING EMERGENCY TO BACKEND!");
  sendEmergencyDataNow();
}

// Add this new function to your ESP32 code:
void sendEmergencyDataNow() {
  if (!wifiConnected) {
    Serial.println("❌ WiFi not connected!");
    return;
  }
  
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("User-Agent", "ESP32HTTPClient/1.0");
  
  // Create emergency JSON payload
  DynamicJsonDocument doc(600);
  doc["device_id"] = deviceID;
  doc["danger"] = true;  // ALWAYS TRUE for ESP-NOW emergency data
  doc["latitude"] = incomingData.lat;  // Use REAL coordinates from ESP-NOW
  doc["longitude"] = incomingData.lon; // Use REAL coordinates from ESP-NOW
  doc["location_name"] = LOCATION_NAME;
  doc["sender_id"] = incomingData.id;
  doc["data_source"] = "esp_now";
  doc["wifi_rssi"] = WiFi.RSSI();
  doc["uptime"] = millis();
  doc["timestamp"] = millis();
  doc["heartbeat"] = false;  // NOT a heartbeat - this is REAL emergency data
  doc["test"] = false;
  doc["free_heap"] = ESP.getFreeHeap();
  doc["chip_id"] = String(ESP.getEfuseMac(), HEX);
  
  String payload;
  serializeJson(doc, payload);
  
  Serial.println("📤 EMERGENCY PAYLOAD:");
  Serial.println(payload);
  
  int httpResponseCode = http.POST(payload);
  
  Serial.print("📡 Response Code: ");
  Serial.println(httpResponseCode);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("✅ EMERGENCY SENT TO BACKEND!");
    Serial.println("Response: " + response);
    
    // Flash LED to confirm
    for (int i = 0; i < 5; i++) {
      digitalWrite(LED_PIN, HIGH);
      delay(100);
      digitalWrite(LED_PIN, LOW);
      delay(100);
    }
  } else {
    Serial.println("❌ FAILED to send emergency!");
  }
  
  http.end();
}

/*
 * INSTRUCTIONS:
 * 1. Replace your OnDataRecv function with the one above
 * 2. Add the sendEmergencyDataNow() function to your code
 * 3. Upload to ESP32
 * 4. Test - you should now see:
 *    - "🚨 SENDING EMERGENCY TO BACKEND!" when ESP-NOW data received
 *    - Backend showing "🚨 Danger Status: 🔴 EMERGENCY!"
 *    - Real coordinates in backend logs
 *    - "💓 Heartbeat: False" (not heartbeat data)
 */