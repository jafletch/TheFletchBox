from abc import ABCMeta

import config

class serialpacket():

    __metaclass__ = ABCMeta

    PACKETSTART = [255, 85]

class requestpacket(serialpacket):
    
    def __init__(self, index, action, device, port, slot = None, data = None):
        self.index = index
        self.action = config.action.validate(action)
        self.device = config.device.validate(device)
        self.port = config.port.validate(port)
        if slot != None:
            self.slot = config.slot.validate(slot)
        else:
            self.slot = None
        self.data = data

    def toByteArray(self):
        length = 4
        if self.slot != None:
            length = length + 1
            if self.data != None:
                length = length + len(self.data)
        bytes = bytearray()
        bytes.extend(serialpacket.PACKETSTART)
        bytes.append(length)
        bytes.append(self.index)
        bytes.append(self.action)
        bytes.append(self.device)
        bytes.append(self.port)
        if self.slot != None:
            bytes.append(self.slot)
        if self.data != None:
            bytes.extend(self.data)

        return bytes
        
class responsepacket(serialpacket):

    def __init__(self, bytes):
        packetlen = len(bytes)
        if packetlen < 2 or bytes[0] != self.PACKETSTART[0] or bytes[1] != self.PACKETSTART[1]:
            raise PacketError("Packet is too short or does not contain start sequence")
        if packetlen >= 3:
            self.index = bytes[2]
        else:
            self.index = None
        if packetlen > 3:
            self.data = bytes[3:]
        else:
            self.data = None

class PacketError(Exception):
    def __init__(self, message):
        super(PacketError, self).__init__(message)