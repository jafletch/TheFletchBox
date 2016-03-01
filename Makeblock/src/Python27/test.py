import config
from devices import *
from orion import *
from packets import responsepacket
from testserial import *
import time

t = temperatureSensor(slot.SLOT_2)
testport = testserial()

board = orion(testport)
board.port1.addDevice(t)

testport.write(bytearray([255, 85, 33, 3, 0, 128, 174, 65, 13, 10]))

latest = t.latestValue()
while latest == -1:
    time.sleep(0.5)
    latest = t.latestValue()

print latest
