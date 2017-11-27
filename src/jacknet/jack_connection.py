from uuid import getnode as get_mac
from jacknet.tools import *
import binascii


class JackConnection:

    def __init__(self, device=None):
        self.mac = get_mac()
        self.device = device

    def send_msg(self, msg, mac):
        data = mac_to_bin(self.mac)
        data += mac_to_bin(mac)
        data += int_to_bin(len(msg))
        data += data_to_bin(msg)
        data += int_to_bin(binascii.crc32(data.encode()))
        self.device.send_msg(data)

    def receive_msg(self):
        data = self.device.get_msg()
        first = bin_to_mac(data[0:8*6])
        second = bin_to_mac(data[8*6:8*12])
        length = bin_to_int(data[8*12:8*16])
        msg = bin_to_data(data[8*16:8*(16 + length)])
        crc = bin_to_int(data[8*(16+length):])
        if binascii.crc32(data[:-(4*8)].encode()) != crc:
            raise TypeError
        return first, second, length, msg, crc

