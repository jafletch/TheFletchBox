from abc import *
from config import *
from packets import *
import struct

class simpledevice():

    __metaclass__ = ABCMeta

    def __init__(self, deviceType):
        self.device = device.validate(deviceType)
        self.port = None
        self.index = None

    @abstractmethod
    def parseData(self, data):
        return False

    def bytesToFloat(self, s ,pos_start):
        d =bytearray(s[pos_start:pos_start+4])
        f = struct.unpack("1f",str(d))[0]
        return f

class slotteddevice(simpledevice):

    __metaclass__ = ABCMeta

    def __init__(self, deviceType, moduleSlot):
        super(slotteddevice, self).__init__(deviceType)
        self.slot = slot.validate(moduleSlot)

class temperatureSensor(slotteddevice):

    def __init__(self, moduleSlot):
        super(temperatureSensor, self).__init__(device.TEMPERATURE_SENSOR, moduleSlot)
        self.__value = -1

    def requestTemp(self):
        self.port.sendRequest(requestpacket(self.index, action.GET, self.device, self.port.id, self.slot))

    def latestValue(self):
        return self.__value

    def parseData(self, data):
        if len(data) != 4:
            raise PacketError("Expected 4 bytes of data returned. Got: " + str(len(data)))
        self.__value = self.bytesToFloat(data, 0)

class lightAndGrayscaleSensor(simpledevice):

    def __init__(self):
        super(lightAndGrayscaleSensor, self).__init__(device.LIGHT_SENSOR)
        self.__value = -1

    def requestValue(self):
        self.port.sendRequest(requestpacket(self.index, action.GET, self.device, self.port.id))

    def latestValue(self):
        return self.__value

    def parseData(self, data):
        if len(data) != 4:
            raise PacketError("Expected 4 bytes of data returned. Got: " + str(len(data)))
        self.__value = self.bytesToFloat(data, 0)

class ultrasonicSensor(simpledevice):

    def __init__(self):
        super(ultrasonicSensor, self).__init__(device.ULTRASONIC_SENSOR)
        self.__value = -1

    def requestValue(self):
        self.port.sendRequest(requestpacket(self.index, action.GET, self.device, self.port.id))

    def latestValue(self):
        return self.__value

    def parseData(self, data):
        if len(data) != 4:
            raise PacketError("Expected 4 bytes of data returned. Got: " + str(len(data)))
        self.__value = self.bytesToFloat(data, 0)