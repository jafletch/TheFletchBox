import config
from devices import *
from orion import *
from packets import responsepacket

t = temperatureSensor(slot.SLOT_2)

board = orion()
board.port1.addDevice(t)

board.handleResponse(bytearray([255, 85, 33, 3, 0, 128, 174, 65, 13, 10]))

print t.latestValue()
