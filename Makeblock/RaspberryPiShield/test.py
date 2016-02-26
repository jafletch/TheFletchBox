import config
from devices import *
from deviceset import *
from packets import responsepacket

t = temperatureSensor(port.PORT_1, slot.SLOT_2)

set = deviceset()
set.addDevice(t)

set.handleResponse(bytearray([255, 85, 0, 0, 128, 174, 65]))

print t.latestValue()
