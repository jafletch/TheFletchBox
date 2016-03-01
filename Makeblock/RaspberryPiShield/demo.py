from config import slot
import logging
from orion import *
import sys
import time

olog = logging.getLogger('orion')
olog.setLevel(logging.INFO)
olog.addHandler(logging.StreamHandler(sys.stdout))

orionBoard = orion()

tempSensor = temperatureSensor(config.slot.SLOT_1)

sevSeg = sevenSegmentDisplay()

orionBoard.port4.addDevice(tempSensor)
orionBoard.port3.addDevice(sevSeg)

lastTemp = tempSensor.latestValue()
while True:
    tempSensor.requestValue()

    curTemp = tempSensor.latestValue()
    if temp != lastTemp:
        sevSeg.setValue(curTemp)

    time.sleep(0.5)