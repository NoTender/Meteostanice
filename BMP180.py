#!/usr/bin/env python
import smbus
import pigpio
import time
from ctypes import c_short

class BMP180:
    def __init__(self,controlLed):
        self.pi= pigpio.pi()
        self.controlLed=controlLed
        self.DEVICE = 0x77  # I2C DEVICEess
        self.bus = smbus.SMBus(1)  # PI version 2
        # Register DEVICEesses
        self.REG_CALIB = 0xAA
        self.REG_MEAS = 0xF4
        self.REG_MSB = 0xF6
        self.REG_LSB = 0xF7
        # Control Register DEVICEess
        self.CRV_TEMP = 0x2E
        self.CRV_PRES = 0x34
        # Oversample setting
        self.OVERSAMPLE = 3  # 0 - 3
        self.data = None
        self.pressure = 0

    def convertToString(self,data):
        return str((data[1] + (256 * data[0])) / 1.2)

    def getShort(self,data, index):
        return c_short((data[index] << 8) + data[index + 1]).value

    def getUshort(self,data, index):
        return (data[index] << 8) + data[index + 1]

    def getPressure(self):
        return self.pressure/100.0

    def update(self):
        self.data = self.bus.read_i2c_block_data(self.DEVICE, self.REG_CALIB, 22)

        self.pi.write(self.controlLed, 1)

        # Convert byte data to word values
        AC1 = self.getShort(self.data, 0)
        AC2 = self.getShort(self.data, 2)
        AC3 = self.getShort(self.data, 4)
        AC4 = self.getUshort(self.data, 6)
        AC5 = self.getUshort(self.data, 8)
        AC6 = self.getUshort(self.data, 10)
        B1 = self.getShort(self.data, 12)
        B2 = self.getShort(self.data, 14)
        MB = self.getShort(self.data, 16)
        MC = self.getShort(self.data, 18)
        MD = self.getShort(self.data, 20)

        # Read pressure
        self.bus.write_byte_data(self.DEVICE, self.REG_MEAS, self.CRV_PRES + (self.OVERSAMPLE << 6))
        time.sleep(0.04)
        (msb, lsb, xsb) = self.bus.read_i2c_block_data(self.DEVICE, self.REG_MSB, 3)
        UP = ((msb << 16) + (lsb << 8) + xsb) >> (8 - self.OVERSAMPLE)

        # Refine pressure
        B6 = 0

        # Refine pressure
        B62 = B6 * B6 >> 12
        X1 = (B2 * B62) >> 11
        X2 = 0 >> 11
        X3 = X1 + X2
        B3 = (((AC1 * 4 + X3) << self.OVERSAMPLE) + 2) >> 2

        X1 = AC3 * B6 >> 13
        X2 = (B1 * B62) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (AC4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * (50000 >> self.OVERSAMPLE)

        P = (B7 * 2) / B4
        X1 = (P >> 8) * (P >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * P) >> 16
        self.pressure = P + ((X1 + X2 + 3791) >> 4)
        self.pi.write(self.controlLed, 0)
