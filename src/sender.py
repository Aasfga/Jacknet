from jacknet.devices.real_jack import RealJack
from jacknet.jack_connection import JackConnection
from uuid import getnode as get_mac

jack = RealJack(0.025)
jc = JackConnection(jack)
jc.send_msg("ABCDEFGHIJKALSDFAF", get_mac())
