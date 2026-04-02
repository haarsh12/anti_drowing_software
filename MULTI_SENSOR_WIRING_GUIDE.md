# ESP32 Multi-Sensor Emergency System Wiring Guide

## Components Required

### Sender Unit:
- ESP32 Development Board
- NRF24L01+PA+LNA Module
- LoRa SX1276/SX1278 Module (433MHz)
- GPS Module (NEO-6M/NEO-8M)
- MPU6050 Gyroscope/Accelerometer
- Emergency Button
- Buzzer (5V/3.3V)
- LEDs
- Battery (Li-Po 3.7V)
- Resistors, Capacitors

### Receiver Unit:
- ESP32 Development Board
- NRF24L01+PA+LNA Module
- LoRa SX1276/SX1278 Module (433MHz)
- Status LEDs

## Wiring Connections

### ESP32 Sender Connections:

#### NRF24L01+PA+LNA Module:
```
NRF24L01    ESP32
VCC      -> 3.3V
GND      -> GND
CE       -> GPIO 4
CSN      -> GPIO 5
SCK      -> GPIO 18
MOSI     -> GPIO 23
MISO     -> GPIO 19
```

#### LoRa Module (SX1276/SX1278):
```
LoRa        ESP32
VCC      -> 3.3V
GND      -> GND
NSS      -> GPIO 18
RST      -> GPIO 14
DIO0     -> GPIO 26
SCK      -> GPIO 18
MOSI     -> GPIO 23
MISO     -> GPIO 19
```

#### GPS Module:
```
GPS         ESP32
VCC      -> 3.3V/5V
GND      -> GND
TX       -> GPIO 16 (RX)
RX       -> GPIO 17 (TX)
```

#### MPU6050:
```
MPU6050     ESP32
VCC      -> 3.3V
GND      -> GND
SDA      -> GPIO 21
SCL      -> GPIO 22
```

#### Other Components:
```
Component       ESP32
Emergency Btn -> GPIO 0 (with pullup)
LED          -> GPIO 2
Buzzer       -> GPIO 25
Battery ADC  -> GPIO 36 (A0)
```

### ESP32 Receiver Connections:

#### NRF24L01+PA+LNA Module:
```
NRF24L01    ESP32
VCC      -> 3.3V
GND      -> GND
CE       -> GPIO 4
CSN      -> GPIO 5
SCK      -> GPIO 18
MOSI     -> GPIO 23
MISO     -> GPIO 19
```

#### LoRa Module:
```
LoRa        ESP32
VCC      -> 3.3V
GND      -> GND
NSS      -> GPIO 18
RST      -> GPIO 14
DIO0     -> GPIO 26
SCK      -> GPIO 18
MOSI     -> GPIO 23
MISO     -> GPIO 19
```

#### Status LEDs:
```
LED Function    ESP32
NRF Status   -> GPIO 12
LoRa Status  -> GPIO 13
WiFi Status  -> GPIO 15
Emergency    -> GPIO 2
```

## Required Libraries

### Arduino IDE Libraries:
```
1. RF24 by TMRh20
2. LoRa by Sandeep Mistry
3. MPU6050 by Electronic Cats
4. ArduinoJson by Benoit Blanchon
5. SoftwareSerial (built-in)
6. WiFi (built-in)
7. HTTPClient (built-in)
```

### Installation Commands:
```bash
# In Arduino IDE Library Manager, search and install:
- "RF24"
- "LoRa"
- "MPU6050"
- "ArduinoJson"
```

## Power Considerations

### NRF24L01+PA+LNA Power:
- Requires stable 3.3V supply
- Peak current: 115mA (transmit)
- Use capacitors (10µF + 100nF) near VCC pin
- Consider external 3.3V regulator for stable operation

### LoRa Module Power:
- Operating voltage: 3.3V
- Peak current: 120mA (transmit at +20dBm)
- Use capacitors for power filtering

### Battery Management:
- Use Li-Po 3.7V battery (2000mAh+ recommended)
- Add voltage divider for battery monitoring
- Consider low-power modes for extended operation

## Range Expectations

### NRF24L01+PA+LNA:
- Line of sight: 1000-1500 meters
- Urban environment: 200-500 meters
- Indoor: 50-100 meters

### LoRa (433MHz):
- Line of sight: 5-15 kilometers
- Urban environment: 1-3 kilometers
- Indoor: 200-500 meters

## Emergency Detection Features

### MPU6050 Triggers:
- High acceleration (>20g) - Impact detection
- High rotation (>250°/s) - Tumbling detection
- Low acceleration (<2g) - Free fall detection
- Sustained abnormal motion (>3 seconds)

### Manual Triggers:
- Emergency button press
- Automatic transmission during emergency
- Visual and audio alerts

## Setup Instructions

### 1. Hardware Assembly:
- Connect all modules according to wiring diagram
- Double-check power connections (3.3V vs 5V)
- Add power filtering capacitors
- Secure all connections

### 2. Software Upload:
- Install required libraries
- Upload sender code to sender ESP32
- Upload receiver code to receiver ESP32
- Configure WiFi credentials in receiver

### 3. Testing:
- Power on both units
- Check serial monitor for initialization messages
- Test emergency button
- Verify data transmission
- Check backend connectivity

### 4. Calibration:
- Adjust emergency detection thresholds
- Test GPS acquisition time
- Verify transmission ranges
- Calibrate battery monitoring

## Troubleshooting

### Common Issues:
1. **NRF24L01 not working**: Check power supply stability, add capacitors
2. **LoRa range issues**: Verify antenna connection, check frequency settings
3. **GPS not fixing**: Ensure clear sky view, check baud rate
4. **MPU6050 errors**: Verify I2C connections, check pull-up resistors
5. **WiFi connection fails**: Check credentials, signal strength

### Debug Tips:
- Use serial monitor for debugging
- Check LED status indicators
- Verify module initialization messages
- Test modules individually
- Check power consumption

## Performance Optimization

### Power Saving:
- Use deep sleep between transmissions
- Reduce transmission frequency when not in emergency
- Optimize sensor reading intervals
- Use low-power GPS modes

### Reliability:
- Implement redundant transmission (NRF + LoRa)
- Add error checking and retransmission
- Use watchdog timers
- Implement failsafe modes

### Range Enhancement:
- Use external antennas
- Optimize antenna placement
- Adjust transmission power
- Consider repeater stations