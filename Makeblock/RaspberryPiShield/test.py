import config
from devices import *

t = temperatureSensor(port.PORT_1, slot.SLOT_2)

f = t.getTemp()