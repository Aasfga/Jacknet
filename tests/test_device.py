import unittest
from _tools import *
from jacknet.tools import *
import random
from jacknet.devices.abstract_device import *

class TestDevice(unittest.TestCase):

    def test_encode_set(self):
        keys = []
        values = []
        for k in encode_set:
            keys.append(k)
            val = encode_set[k]
            values.append(val)
            self.assertGreaterEqual(sum([int(x) for x in val]), 2)
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(len(values), len(set(values)))

    def test_sets(self):
        for k in encode_set:
            self.assertEqual(k, decode_set[encode_set[k]])


if __name__ == '__main__':
    unittest.main()