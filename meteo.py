import argparse
import smbus
import time
from ctypes import c_short
import pigpio
from DHT22 import DHT22
from BMP180 import BMP180

if __name__ == "__main__":
    # This parser allows to process multiple occurences of one argument and its value. The last value given by argument is taken.
    parser = argparse.ArgumentParser(
        description='Application for processing data from temperature, pressure and humidity sensors.')
    parser.add_argument('--time', '-t', default=500, type=int,
                        help='Time in miliseconds. This value specifies sample rate. Default value is 500 ms.')
    parser.add_argument('--number', '-n', default=10, type=int,
                        help='Number of samples for processing. Default value is 5 samples for each sensor.')

    args = parser.parse_args()
    # default GPIO setup
    bmp180 = BMP180(22)
    dht22 = DHT22(17, 27)
    i = 0
    SLEEP_INTERVAL = args.time / 1000.0

    while i < args.number:
        bmp180.update()
        dht22.update()
        time.sleep(SLEEP_INTERVAL)
        print(bmp180.getPressure(), dht22.getTemperature(), dht22.getHumidity())
        i += 1
    dht22.destroy()
