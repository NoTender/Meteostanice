#!/usr/bin/env python
import argparse
import time
import csv
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
    csvWriter=csv.writer(open('out.csv','a'),delimiter=',')

    while i < args.number:
        bmp180.update()
        dht22.update()
        time.sleep(SLEEP_INTERVAL)
        print(time.time(),float("%.2f" % dht22.getTemperature()),float("%.2f" % bmp180.getPressure()),float("%.2f" % dht22.getHumidity()))
        csvWriter.writerow([time.time(),float("%.2f" % dht22.getTemperature()),float("%.2f" % bmp180.getPressure()),float("%.2f" % dht22.getHumidity())])
        i += 1
    dht22.destroy()

