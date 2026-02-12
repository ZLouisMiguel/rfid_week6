# boot.py - ESP8266 boot configuration
# Team: y2c_grp125

import gc
import network
import time

gc.enable()

print("\n" + "="*50)
print("RFID Top-Up System - Team y2c_grp125")
print("="*50 + "\n")

# Configure LED
from machine import Pin
led = Pin(2, Pin.OUT)
led.value(1)  # OFF (active low)

print("Boot complete. Running main.py...\n")