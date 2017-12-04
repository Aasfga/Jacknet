from uuid import getnode as get_mac

from jacknet.devices.buffered_jack import BufferedJack
from jacknet.jack_connection import JackConnection
import binascii
import zlib


bj = BufferedJack(0.03)
jc = JackConnection(bj)
jc.send_msg("ABCDEDF", get_mac())
print(jc.receive_msg())
