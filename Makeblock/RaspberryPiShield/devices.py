from abc import ABCMeta

from config import *

from serial_packet import serial_packet

class simpledevice():

    __metaclass__ = ABCMeta

    def __init__(self, deviceType, modulePort):
        self.device = device.validate(deviceType)
        self.port = port.validate(modulePort)

class slotteddevice(simpledevice):

    __metaclass__ = ABCMeta

    def __init__(self, deviceType, modulePort, moduleSlot):
        super(slottedmodule, self).__init__(deviceType, modulePort)
        self.slot = slot.validate(moduleSlot)

class temperatureSensor(slotteddevice):

    def __init__(self, modulePort, moduleSlot):
        super(temperatureSensor, self).__init__(device.TEMPERATURE_SENSOR, modulePort, moduleSlot)

    def getTemp(self):
        return serial_packet(5, 0, action.GET, self.device, self.port, self.slot).toByteArray()