import unittest

from _tools import random_word
from jacknet.devices.buffered_jack import BufferedJack
from jacknet.jack_connection import JackConnection
from uuid import getnode as get_mac


class TestBufferedJack(unittest.TestCase):
    def test_communication(self):
        bj = BufferedJack(0.03)
        jc = JackConnection(bj)

        for i in range(10):
            word = random_word(30)
            jc.send_msg(word, get_mac())
            first, second, length, data, crc = jc.receive_msg()
            self.assertEqual(word, data)


if __name__ == '__main__':
    unittest.main()
