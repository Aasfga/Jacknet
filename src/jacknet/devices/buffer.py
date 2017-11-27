from jacknet.devices import *


class BufferDevice(AbstractDevice):
    def __init__(self):
        self.buffer = ""

    def send_msg(self, data):
        self.buffer = self.conv4b5b(data)

    def get_msg(self):
        return self.conv5b4b(self.buffer)