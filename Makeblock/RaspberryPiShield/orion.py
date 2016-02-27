from abc import ABCMeta
import config
from devices import *
import exceptions
from packets import responsepacket
import serial
import threading

class board():
    __metaclass__ = ABCMeta

    def __init__(self, dataHandler):
        ser = serial.Serial('/dev/ttyAMA0', 115200)
        th = serialRead(dataHandler)
        th.setDaemon(True)
        th.start()

    class serialRead(threading.Thread):
        
        def __init__(self, dataHandler):
            threading.Thread.__init__(self)
            self.dataHandler = dataHandler
    
        def run(self):
            while True:
                line = ser.readline()
                self.dataHandler(map(ord,line))

class orion(board):
    
    def __init__(self):
        super(orion, self).__init__(self.handleResponse)
        self.port1 = port(self, config.port.PORT_1)
        self.port2 = port(self, config.port.PORT_2)
        self.port3 = port(self, config.port.PORT_3)
        self.port4 = port(self, config.port.PORT_4)
        self.port5 = port(self, config.port.PORT_5)
        self.port6 = port(self, config.port.PORT_6)
        self.port7 = port(self, config.port.PORT_7)
        self.port8 = port(self, config.port.PORT_8)
        self.motor1 = port(self, config.port.MOTOR_1)
        self.motor2 = port(self, config.port.MOTOR_2)
        self.__ports = {
                        config.port.PORT_1 : self.port1,
                        config.port.PORT_2 : self.port2,
                        config.port.PORT_3 : self.port3,
                        config.port.PORT_4 : self.port4,
                        config.port.PORT_5 : self.port5,
                        config.port.PORT_6 : self.port6,
                        config.port.PORT_7 : self.port7,
                        config.port.PORT_8 : self.port8,
                        config.port.MOTOR_1 : self.motor1,
                        config.port.MOTOR_2 : self.motor2,
                       }

    def handleResponse(self, bytes):
        response = responsepacket(bytes)
        # skip invalid packets
        if not response.valid:
            return

        (portNumber, slotNumber) = orion.__unpackIndex(response.index)
        responsePort = self.__ports[portNumber]
        if responsePort.occupied:
            responsePort.getDevice(slotNumber).parseData(response.data)

    @staticmethod
    def __unpackIndex(byte):
        return (byte & 15, byte >> 4 & 15)

class port(object):
    
    def __init__(self, board, portNumber):
        self.__board = board
        self.id = config.port.validate(portNumber)
        self.__occupied = False
        self.__devices = []

    @property
    def occupied(self):
        return self.__occupied

    def addDevice(self, device):
        self.__occupied = True

        if device.slot == None and len(self.__devices) > 0:
            raise BoardError("Port %s is already occupied" % str(self.id))

        if device.slot != None:
            if len(self.__devices) >= 2:
                raise BoardError("Port %s is already occupied" % str(self.id))
            for d in self.__devices:
                if d.slot == device.slot:
                    raise BoardError("Port %s, slot %s is already occupied" % (str(self.id), device.slot))

        self.__devices.append(device)

        device.port = self.id
        device.index = device.port
        if device.slot != None:
            device.index = device.index + (device.slot << 4)

    def getDevice(self, slot = None):
        if slot == None or slot == 0:
            return self.__devices[0]
        for d in self.__devices:
            if d.slot == slot:
                return d

class BoardError(Exception):
    def __init__(self, message):
        super(BoardError, self).__init__(message)