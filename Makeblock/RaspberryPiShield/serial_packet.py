import config

class serial_packet(object):
    """description of class"""

    PACKETSTART = [255, 85]

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
        bytes.extend(serial_packet.PACKETSTART)
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
        
