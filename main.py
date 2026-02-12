# test_no_wifi.py - NO WIFI, JUST RFID
from machine import Pin, SPI, SoftSPI
from mfrc522 import MFRC522
import time

print("\nRFID TEST - NO WIFI, NO MQTT")
print("This should NOT reset\n")

sck = Pin(14, Pin.OUT)
mosi = Pin(13, Pin.OUT)
miso = Pin(12, Pin.OUT)
cs = Pin(2, Pin.OUT)
rst = Pin(0, Pin.OUT)

spi = SoftSPI(baudrate=100000, sck=sck, mosi=mosi, miso=miso)
rfid = MFRC522(spi, cs, rst)

# Boost antenna
try:
    rfid._wreg(0x26, 0x8D)
    rfid._wreg(0x14, 0x12)
    print("Antenna boosted")
except: pass

print("\nREADY - Tap card")
print("="*40)

while True:
    try:
        stat, _ = rfid.request(rfid.REQIDL)
        if stat == rfid.OK:
            stat, uid_raw = rfid.anticoll()
            if stat == rfid.OK:
                uid = ''.join([f"{x:02X}" for x in uid_raw])
                if uid != "00000000":
                    print(f"\n✅ CARD DETECTED!")
                    print(f"   UID: {uid}")
        time.sleep(0.3)
    except Exception as e:
        print(f"Error: {e}")