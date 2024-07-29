# GENERAL INFORMATION

The purpose of this project is to create advertisement robot using ESP32 and Raspberry Pi Pico microprocessors. 
Mentioned boards are used for the sound effects (ESP32) and steering DC Motors through Access Point (Raspberry Pi Pico).

# COMPONENTS

Components used in the project:
- ESP32 S3 N16R8 DevKitC-1 16MB Flash 8MB PSRAM 2 x USB C
- Raspberry Pi Pico W - RP2040 ARM Cortex M0+ CYW43439 - WiFi
- MciroSD reader board

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
- SD library made by Arduino (for some IDEs it is not needed)

**MicroSD card adjustments:**
- .mp3 file format
- 256kbps quality
- 44.1 kHz sample rate
- Mono channel for better sound (not necessary!)

For working audio mp3 converter check out the **Useful links** section.

# CIRCUIT DIAGRAM

The circuit diagrams for both Raspberry and ESP32 is shown in my Github: https://github.com/sailor-elite

# INSTALLATION

1. Connect electronic parts for ESP32 and Raspberry boards using given circuit diagrams
2. Insert MicroSD card with your own mp3 files (Remember to adjust proper settings which are mentioned in the **Dependencies** section)
3. Upload the main.cpp code from audioesp folder to ESP32 board
4. Upload the ______ code from _________ folder to Raspberry board
5. Click the reset button for both boards
6. It should be ready to go! 

# USEFUL LINKS
https://onlineaudioconverter.com/#