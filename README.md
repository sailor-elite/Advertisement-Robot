# GENERAL INFORMATION

The purpose of this project is to create advertisement robot using ESP32 and Raspberry Pi Pico microprocessors. 
Mentioned boards are used for the sound effects (ESP32) and steering DC Motors through Access Point (Raspberry Pi Pico W).

# COMPONENTS

Components used in the project:
- ESP32 S3 N16R8 DevKitC-1 16MB Flash 8MB PSRAM 2 x USB C
- Raspberry Pi Pico W - RP2040 ARM Cortex M0+ CYW43439 - WiFi
- MicroSD reader board

# DEPENDENCIES

**CODING LANGUAGE:**
- C++
- Python

**IDE:**
- Visual Studio Code
- PlatformIO

**Libriaries:**
- Default Arduino Libraries
- AudioI2S library made by schreibfaul1
- SD library made by Arduino

**Audio file adjustments:**
- .mp3 file format
- 256kbps quality
- 44.1 kHz sample rate
- Mono channel for better sound (not necessary)

For working audio mp3 converter check out the **Useful links** section.

# CIRCUIT DIAGRAM
DC Motor Steering Schematic: ![PicoMotorCircuitDiagram_bb](https://github.com/user-attachments/assets/099b944c-4642-492b-b489-c555d795320a)
Audio Schematic: ![Esp32Audio_bb](https://github.com/user-attachments/assets/04ebd0ec-229a-4bcf-8707-837bba1134ac) 
Power supply Schematic: ![PowerSupplyCircuit_bb](https://github.com/user-attachments/assets/907c398e-a168-46ea-b94d-b6abd995351c)
# INSTALLATION

1. Connect electronic parts for ESP32 and Raspberry boards using given circuit diagrams
2. Insert MicroSD card with your own mp3 files (Remember to adjust proper settings which are mentioned in the **Dependencies** section)
3. Upload the *main.cpp* code from *audioesp* folder to ESP32 board
4. Upload the *main.py* code from *picomotorcontrol* folder to Raspberry Pi Pico W's board
5. Connect to the custom Raspberry Pi Pico W Access Point
6. Copy the Raspbery Pi Pico W's Access Point IP adress (192.168.4.1) and paste it on the web browser
7. It should be ready to go! 

# USEFUL LINKS
https://onlineaudioconverter.com/#
