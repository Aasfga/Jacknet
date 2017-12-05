from jacknet.devices.real_jack import RealJack
from jacknet.jack_connection import JackConnection

jack = RealJack(0.025)
jc = JackConnection(jack)
print(jc.receive_msg())
