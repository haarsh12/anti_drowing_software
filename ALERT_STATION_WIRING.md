# Emergency Alert Station Wiring Guide

## Components Required
- ESP32 Development Board
- NRF24L01+PA+LNA Module
- LoRa SX1276/SX1278 Module (433MHz)
- Active Buzzer (5V or 3.3V)
- LEDs (4x)
- Push Button
- Resistors (220Ω for LEDs, 10kΩ for button)
- Breadboard/PCB
- Power Supply (5V/3.3V)

## Pin Connections

### ESP32 Alert Station Connections:

```
Component       ESP32 Pin    Notes
================================
NRF24L01 VCC -> 3.3V         Stable power required
NRF24L01 GND -> GND
NRF24L01 CE  -> GPIO 4
NRF24L01 CSN -> GPIO 5
NRF24L01 SCK -> GPIO 18      SPI Clock
NRF24L01 MOSI-> GPIO 23      SPI Data Out
NRF24L01 MISO-> GPIO 19      SPI Data In

LoRa VCC     -> 3.3V         
LoRa GND     -> GND
LoRa NSS     -> GPIO 18      Chip Select
LoRa RST     -> GPIO 14      Reset
LoRa DIO0    -> GPIO 26      Interrupt
LoRa SCK     -> GPIO 18      SPI Clock (shared)
LoRa MOSI    -> GPIO 23      SPI Data Out (shared)
LoRa MISO    -> GPIO 19      SPI Data In (shared)

Buzzer +     -> GPIO 25      Active buzzer
Buzzer -     -> GND

LED Emergency-> GPIO 2       Red LED + 220Ω resistor
LED NRF      -> GPIO 12      Green LED + 220Ω resistor  
LED LoRa     -> GPIO 13      Blue LED + 220Ω resistor
LED Power    -> GPIO 15      White LED + 220Ω resistor

Button       -> GPIO 0       Button + 10kΩ pullup to 3.3V
Button GND   -> GND
```

## LED Indicators

### Status LEDs:
- **Red (GPIO 2)**: Emergency Alert Active
- **Green (GPIO 12)**: NRF24L01 Status
- **Blue (GPIO 13)**: LoRa Status  
- **White (GPIO 15)**: Power/Heartbeat

### LED Behavior:
- **Solid ON**: Module working normally
- **Blinking**: Data received/activity
- **OFF**: Module error or inactive
- **Fast Flash**: Emergency alert active

## Buzzer Patterns

### Alert Patterns:
- **Emergency**: Fast beeps (200ms ON, 100ms OFF) x3, then 500ms pause
- **Warning**: Slow beeps (500ms ON, 500ms OFF)
- **Confirmation**: Quick beeps (100ms ON, 50ms OFF) x3

### Emergency Sequence:
1. **Immediate**: 10 fast beeps when emergency detected
2. **Continuous**: Repeat emergency pattern every 3 seconds
3. **Silence**: Press button once to silence buzzer (LED stays on)
4. **Reset**: Press button again to clear all alerts

## Power Requirements

### Current Consumption:
- ESP32: 80-240mA (active)
- NRF24L01+PA: 115mA (transmit), 13.5mA (receive)
- LoRa: 120mA (transmit), 10mA (receive)
- Buzzer: 20-50mA (active)
- LEDs: 20mA each (4x = 80mA max)

### Total: ~300-500mA peak, ~150mA average

### Power Supply Options:
- USB 5V (recommended for development)
- 5V wall adapter (2A minimum)
- 12V with voltage regulator
- Battery pack (6x AA = 9V with regulator)

## Assembly Instructions

### 1. Breadboard Layout:
```
Power Rails:
- Top rail: 3.3V
- Bottom rail: GND

Left Side:
- ESP32 module
- Power connections

Center:
- NRF24L01 module
- LoRa module

Right Side:
- LEDs with resistors
- Buzzer
- Button with pullup
```

### 2. SPI Bus Sharing:
Both NRF24L01 and LoRa use SPI bus:
- **Shared**: SCK (18), MOSI (23), MISO (19)
- **Individual**: CS pins (NRF CSN=5, LoRa NSS=18)

### 3. Power Distribution:
- Use breadboard power rails
- Add 100µF capacitor near ESP32 VIN
- Add 10µF + 100nF capacitors near NRF24L01 VCC
- Add 10µF capacitor near LoRa VCC

### 4. Wiring Order:
1. Power connections first (3.3V, GND)
2. SPI bus (shared pins)
3. Individual control pins
4. LEDs with current limiting resistors
5. Buzzer and button

## Testing Procedure

### 1. Power On Test:
- All LEDs should light up briefly
- Buzzer should beep once
- Serial monitor shows "Alert Receiver Ready"

### 2. Module Test:
- Green LED (NRF) should be ON if NRF24L01 working
- Blue LED (LoRa) should be ON if LoRa working
- White LED (Power) should blink every 10 seconds

### 3. Button Test:
- Press button when no alert active
- Should perform system test (LEDs blink, buzzer beeps)
- Serial monitor shows system status

### 4. Communication Test:
- Use sender device to transmit emergency
- Should receive data and trigger alert
- Red LED flashes, buzzer sounds emergency pattern

## Troubleshooting

### No LEDs Light Up:
- Check power connections
- Verify 3.3V voltage at ESP32
- Check ESP32 is programmed correctly

### NRF24L01 Not Working (Green LED OFF):
- Check SPI connections (SCK, MOSI, MISO)
- Verify CE and CSN pins
- Add power filtering capacitors
- Check 3.3V power (NRF24L01 is 3.3V only)

### LoRa Not Working (Blue LED OFF):
- Check SPI connections
- Verify NSS, RST, DIO0 pins
- Check antenna connection
- Verify frequency setting (433MHz)

### No Buzzer Sound:
- Check buzzer polarity
- Verify GPIO 25 connection
- Test with multimeter (should see 3.3V when active)
- Try different buzzer (active vs passive)

### Button Not Responding:
- Check pullup resistor (10kΩ to 3.3V)
- Verify GPIO 0 connection
- Test button continuity
- Check for proper debouncing in code

## Range Testing

### Expected Ranges:
- **NRF24L01+PA+LNA**: 500-1500m (line of sight)
- **LoRa 433MHz**: 2-10km (line of sight)

### Range Test Procedure:
1. Place alert station at fixed location
2. Walk away with sender device
3. Test emergency button at various distances
4. Note maximum reliable range for each protocol
5. Test in different environments (indoor/outdoor/urban)

## Enclosure Recommendations

### Weatherproof Enclosure:
- IP65 rated plastic box
- Ventilation holes for buzzer
- Clear window for LED visibility
- External antenna connectors
- Cable glands for power

### Mounting Options:
- Wall mount bracket
- Pole mount clamp
- Desktop stand
- Magnetic base (for metal surfaces)