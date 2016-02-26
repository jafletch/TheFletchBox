
from rpi_serial import *

while True:
	time.sleep(1)
	distance = doTemperature("Port4", "Slot2")
	print "distance",distance
