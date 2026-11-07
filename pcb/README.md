# OpenLoom PCB schematic connections

This is the wiring represented in `openloom.kicad_sch`. It uses the common
ESP32 DevKit V1 header names; verify the silkscreen and module revision before
powering the circuit. The OLED is a 3.3 V I²C SSD1306 module (typically address
`0x3C`). Buttons use the ESP32 internal pull-ups and therefore short their GPIO
to ground when pressed.

| From | To |
|---|---|
| ESP32 DevKit 3V3 | OLED VCC |
| ESP32 DevKit GND | OLED GND, both button ground contacts, buzzer negative |
| ESP32 GPIO21 | OLED SDA |
| ESP32 GPIO22 | OLED SCL |
| ESP32 GPIO18 | FLIP button signal contact; other contact to GND |
| ESP32 GPIO19 | NEXT button signal contact; other contact to GND |
| ESP32 GPIO23 | Active buzzer positive (+) |

Use a buzzer suitable for direct 3.3 V GPIO drive; otherwise add a suitable
transistor driver. Connect the ESP32 USB connector to the matching USB cable.
