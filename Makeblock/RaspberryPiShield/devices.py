from abc import *

from config import *

from packets import *

import struct

class simpledevice():

    __metaclass__ = ABCMeta

    def __init__(self, deviceType, modulePort):
        self.device = device.validate(deviceType)
        self.index = None
        self.port = port.validate(modulePort)

    @abstractmethod
    def parseData(self, data):
        return False

    def bytesToFloat(self, s ,pos_start):
        d =bytearray(s[pos_start:pos_start+4])
        f = struct.unpack("1f",str(d))[0]
        return f

class slotteddevice(simpledevice):

    __metaclass__ = ABCMeta

    def __init__(self, deviceType, modulePort, moduleSlot):
        super(slotteddevice, self).__init__(deviceType, modulePort)
        self.slot = slot.validate(moduleSlot)

class temperatureSensor(slotteddevice):

    def __init__(self, modulePort, moduleSlot):
        super(temperatureSensor, self).__init__(device.TEMPERATURE_SENSOR, modulePort, moduleSlot)
        self.__value = -1

    def requestTemp(self):
        return requestpacket(self.index, action.GET, self.device, self.port, self.slot).toByteArray()

    def latestValue(self):
        return self.__value

    def parseData(self, data):
        if len(data) != 4:
            raise PacketError("Expected 4 bytes of data returned. Got: " + len(data))
        self.__value = self.bytesToFloat(data, 0)