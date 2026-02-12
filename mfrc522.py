"""
MicroPython MFRC522 RFID reader library.
"""
from machine import Pin, SPI
import time

class MFRC522:
    OK = 0
    NOTAG = 1
    ERR = 2
    
    REQIDL = 0x26
    REQALL = 0x52
    AUTHENT1A = 0x60
    AUTHENT1B = 0x61
    
    def __init__(self, spi, cs, rst):
        self.spi = spi
        self.cs = cs
        self.rst = rst
        self.cs.init(Pin.OUT, value=1)
        self.rst.init(Pin.OUT, value=0)
        self.init()
    
    def _wreg(self, reg, val):
        self.cs.value(0)
        self.spi.write(b'%c' % ((reg << 1) & 0x7E))
        self.spi.write(b'%c' % val)
        self.cs.value(1)
    
    def _rreg(self, reg):
        self.cs.value(0)
        self.spi.write(b'%c' % (((reg << 1) & 0x7E) | 0x80))
        val = self.spi.read(1)[0]
        self.cs.value(1)
        return val
    
    def _sflags(self, reg, mask):
        self._wreg(reg, self._rreg(reg) | mask)
    
    def _cflags(self, reg, mask):
        self._wreg(reg, self._rreg(reg) & (~mask))
    
    def init(self):
        self.rst.value(1)
        self._wreg(0x01, 0x0F)
        self._wreg(0x2A, 0x8D)
        self._wreg(0x2B, 0x3E)
        self._wreg(0x2C, 0x00)
        self._wreg(0x2D, 0x30)
        self._wreg(0x2E, 0x00)
        self._wreg(0x2F, 0x00)
        self._wreg(0x0A, 0x30)
        self._wreg(0x0A, 0x03)
        self._wreg(0x23, 0x8D)
        self._wreg(0x24, 0x3E)
        self._wreg(0x25, 0x00)
        self._wreg(0x26, 0x30)
        self._wreg(0x27, 0x00)
        self._wreg(0x28, 0x00)
        self._wreg(0x29, 0x00)
        self._wreg(0x2C, 0x00)
        self._wreg(0x0C, 0x00)
        self._wreg(0x0D, 0x00)
        self._wreg(0x0E, 0x00)
        self._wreg(0x0F, 0x00)
        self._wreg(0x10, 0x00)
        self._wreg(0x11, 0x00)
        self._wreg(0x12, 0x00)
        self._wreg(0x13, 0x00)
        self._wreg(0x14, 0x00)
        self._wreg(0x15, 0x00)
        self._wreg(0x16, 0x00)
        self._wreg(0x17, 0x00)
        self._wreg(0x18, 0x00)
        self._wreg(0x19, 0x00)
        self._wreg(0x1A, 0x00)
        self._wreg(0x1B, 0x00)
        self._wreg(0x1C, 0x00)
        self._wreg(0x1D, 0x00)
        self._wreg(0x1E, 0x00)
        self._wreg(0x1F, 0x00)
        self._wreg(0x20, 0x00)
        self._wreg(0x21, 0x00)
        self._wreg(0x22, 0x00)
        self._wreg(0x23, 0x00)
        self._wreg(0x24, 0x00)
        self._wreg(0x25, 0x00)
        self._wreg(0x26, 0x00)
        self._wreg(0x27, 0x00)
        self._wreg(0x28, 0x00)
        self._wreg(0x29, 0x00)
        self._wreg(0x2A, 0x00)
        self._wreg(0x2B, 0x00)
        self._wreg(0x2C, 0x00)
        self._wreg(0x2D, 0x00)
        self._wreg(0x2E, 0x00)
        self._wreg(0x2F, 0x00)
        self._wreg(0x30, 0x00)
        self._wreg(0x31, 0x00)
        self._wreg(0x32, 0x00)
        self._wreg(0x33, 0x00)
        self._wreg(0x34, 0x00)
        self._wreg(0x35, 0x00)
        self._wreg(0x36, 0x00)
        self._wreg(0x37, 0x00)
        self._wreg(0x38, 0x00)
        self._wreg(0x39, 0x00)
        self._wreg(0x3A, 0x00)
        self._wreg(0x3B, 0x00)
        self._wreg(0x3C, 0x00)
        self._wreg(0x3D, 0x00)
        self._wreg(0x3E, 0x00)
        self._wreg(0x3F, 0x00)
    
    def request(self, mode):
        self._wreg(0x0D, 0x07)
        self._wreg(0x0C, 0x00)
        self._wreg(0x0E, 0x00)
        self._wreg(0x0D, mode)
        self._wreg(0x0E, 0x00)
        self._sflags(0x04, 0x80)
        self._sflags(0x02, 0x01)
        i = 1000
        while i > 0:
            n = self._rreg(0x04)
            i -= 1
            if not (n & 0x80):
                break
        self._cflags(0x04, 0x80)
        if i == 0:
            return self.ERR, 0
        n = self._rreg(0x0A)
        if n & 0x10:
            return self.ERR, 0
        if n & 0x08:
            return self.NOTAG, 0
        return self.OK, (self._rreg(0x0E) << 8) | self._rreg(0x0F)
    
    def anticoll(self):
        self._wreg(0x0D, 0x93)
        self._wreg(0x0E, 0x20)
        self._sflags(0x04, 0x80)
        self._sflags(0x02, 0x01)
        i = 1000
        while i > 0:
            n = self._rreg(0x04)
            i -= 1
            if not (n & 0x80):
                break
        self._cflags(0x04, 0x80)
        if i == 0:
            return self.ERR, 0
        n = self._rreg(0x0A)
        if n & 0x10:
            return self.ERR, 0
        if n & 0x08:
            return self.NOTAG, 0
        uid = []
        uid.append(self._rreg(0x01))
        uid.append(self._rreg(0x02))
        uid.append(self._rreg(0x03))
        uid.append(self._rreg(0x04))
        bcc = self._rreg(0x05)
        if uid[0] ^ uid[1] ^ uid[2] ^ uid[3] != bcc:
            return self.ERR, 0
        return self.OK, uid
    
    def auth(self, auth_mode, block, key, uid):
        buf = [0x00] * 12
        buf[0] = auth_mode
        buf[1] = block
        for i in range(6):
            buf[i+2] = key[i]
        for i in range(4):
            buf[i+8] = uid[i]
        self._wreg(0x0D, 0x86)
        self._wreg(0x0E, 0x0C)
        for i in range(12):
            self._wreg(0x01 + i, buf[i])
        self._sflags(0x04, 0x80)
        self._sflags(0x02, 0x01)
        i = 1000
        while i > 0:
            n = self._rreg(0x04)
            i -= 1
            if not (n & 0x80):
                break
        self._cflags(0x04, 0x80)
        if i == 0:
            return self.ERR
        n = self._rreg(0x0A)
        if n & 0x10:
            return self.ERR
        if n & 0x08:
            return self.NOTAG
        return self.OK
    
    def stop_crypto(self):
        self._cflags(0x08, 0x08)
    
    def read(self, block):
        buf = [0x00] * 4
        buf[0] = 0x30
        buf[1] = block
        self._wreg(0x0D, 0x86)
        self._wreg(0x0E, 0x04)
        for i in range(4):
            self._wreg(0x01 + i, buf[i])
        self._sflags(0x04, 0x80)
        self._sflags(0x02, 0x01)
        i = 1000
        while i > 0:
            n = self._rreg(0x04)
            i -= 1
            if not (n & 0x80):
                break
        self._cflags(0x04, 0x80)
        if i == 0:
            return None
        n = self._rreg(0x0A)
        if n & 0x10:
            return None
        if n & 0x08:
            return None
        data = []
        for i in range(16):
            data.append(self._rreg(0x01 + i))
        return data
    
    def write(self, block, data):
        buf = [0x00] * 4
        buf[0] = 0xA0
        buf[1] = block
        self._wreg(0x0D, 0x86)
        self._wreg(0x0E, 0x04)
        for i in range(4):
            self._wreg(0x01 + i, buf[i])
        self._sflags(0x04, 0x80)
        self._sflags(0x02, 0x01)
        i = 1000
        while i > 0:
            n = self._rreg(0x04)
            i -= 1
            if not (n & 0x80):
                break
        self._cflags(0x04, 0x80)
        if i == 0:
            return False
        n = self._rreg(0x0A)
        if n & 0x10:
            return False
        if n & 0x08:
            return False
        for i in range(16):
            self._wreg(0x01 + i, data[i])
        self._sflags(0x04, 0x80)
        self._sflags(0x02, 0x01)
        i = 1000
        while i > 0:
            n = self._rreg(0x04)
            i -= 1
            if not (n & 0x80):
                break
        self._cflags(0x04, 0x80)
        if i == 0:
            return False
        n = self._rreg(0x0A)
        if n & 0x10:
            return False
        if n & 0x08:
            return False
        return True