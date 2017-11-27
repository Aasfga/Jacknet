from uuid import getnode as get_mac
from jacknet import *
import binascii
import zlib

bj = BufferedJack(0.03)
jc = JackConnection(bj)
jc.send_msg("ABCDEFGHIJKALSDFAF", get_mac())
print(jc.receive_msg())