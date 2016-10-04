import argparse

#This parser allows to process multiple occurences of one argument and its value. The last value given by argument is taken.
parser = argparse.ArgumentParser(description='Application for processing data from temperature, pressure and humidity sensors.')
parser.add_argument('--time', '-t', default=1000, type=int, help='Time in miliseconds. This value specifies sample rate. Default value is 1000 ms.')
parser.add_argument('--number', '-n', default=5, type=int, help='Number of samples for processing. Default value is 5 samples for each sensor.')

args = parser.parse_args()

print('Time: ' + str(args.time))
print('Number: ' + str(args.number))