from config import actions
from config import devices

class serial_packet(object):
    """description of class"""

    PACKETSTART = [255, 55]

    def __init__(self, index, action, device, port, slot = None, data = None):
        self.index = index
        self.action = actions.validate(action)
        self.device = devices.validate(device)
        self.port = port
        self.slot = slot
        self.data = data

    def toByteArray(self):
        length = 5
        if self.slot != None:
            length = length + 1
            if self.data != None:
                length = length + len(self.data)
        bytes = bytearray()
        bytes.extend(PACKETSTART)
        bytes.append(length)
        bytes.append(self.index)
        bytes.append(self.action)
        bytes.append(self.device)
        bytes.append(self.port)
        bytes.append(self.slot)
        bytes.extend(self.data)

        return bytes
        
