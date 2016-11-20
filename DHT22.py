#!/usr/bin/env python
import pigpio
import time
class DHT22:
    def __init__(self,gpio, controlLed):
        self.pi = pigpio.pi()
        self.gpio = gpio
        self.controlLed = controlLed
        self.cb = None  # set callback function

        self.hmd = -999
        self.temp = -999

        self.tov = None
        self.high_tick = 0
        self.bit = 40  # how many bits we accept

        self.pi.set_pull_up_down(gpio, pigpio.PUD_OFF)

        self.pi.set_watchdog(gpio, 0)

        self.cb = self.pi.callback(gpio, pigpio.EITHER_EDGE, self._callback)

    def _callback(self, gpio, level, tick):

        diff = pigpio.tickDiff(self.high_tick, tick)

        # Edge length determines if bit is 1 or 0.
        if level == 0:
            if diff >= 50:
                val = 1
                if diff >= 200:  # Bad bit?
                    self.CS = 256  # Force bad checksum.
            else:
                val = 0

            if self.bit >= 40:  # Message complete.
                self.bit = 40

            elif self.bit >= 32:  # In checksum byte.
                self.CS = (self.CS << 1) + val

                if self.bit == 39:

                    # 40th bit received.
                    self.pi.set_watchdog(self.gpio, 0)

                    total = self.hH + self.hL + self.tH + self.tL

                    if (total & 255) == self.CS:  # Is checksum ok?

                        self.hmd = ((self.hH << 8) + self.hL) * 0.1

                        if self.tH & 128:  # Negative temperature.
                            mult = -0.1
                            self.tH = self.tH & 127
                        else:
                            mult = 0.1

                        self.temp = ((self.tH << 8) + self.tL) * mult

                        self.tov = time.time()

                        if self.controlLed is not None:
                            self.pi.write(self.controlLed, 0)

            elif self.bit >= 24:  # in temp low byte
                self.tL = (self.tL << 1) + val

            elif self.bit >= 16:  # in temp high byte
                self.tH = (self.tH << 1) + val

            elif self.bit >= 8:  # in humidity low byte
                self.hL = (self.hL << 1) + val

            elif self.bit >= 0:  # in humidity high byte
                self.hH = (self.hH << 1) + val

            self.bit += 1

        elif level == 1:
            self.high_tick = tick
            if diff > 250000:
                self.bit = -2
                self.hH = 0
                self.hL = 0
                self.tH = 0
                self.tL = 0
                self.CS = 0

        else:  # level == pigpio.TIMEOUT:
            self.pi.set_watchdog(self.gpio, 0)

    def getTemperature(self):
        return self.temp

    def getHumidity(self):
        return self.hmd

    def update(self):
        self.pi.write(self.controlLed, 1)
        self.pi.write(self.gpio, pigpio.LOW)
        time.sleep(0.020)  # 20 ms
        self.pi.set_mode(self.gpio, pigpio.INPUT)
        self.pi.set_watchdog(self.gpio, 200)

    def destroy(self):
        self.pi.set_watchdog(self.gpio, 0)
        self.cb = None
        self.pi.stop()



