from devices import *
from packets import responsepacket

class deviceset(object):
        
    def __init__(self):
        self.__devices = dict()

    def addDevice(self, device):
        index = len(self.__devices)
        self.__devices[index] = device
        device.index = index

    def getDevice(self, index):
        return self.__devices[index]

    def handleResponse(self, bytes):
        response = responsepacket(bytes)
        self.__devices[response.index].parseData(response.data)