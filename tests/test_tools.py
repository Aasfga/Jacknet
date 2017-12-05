import unittest
from _tools import *
from jacknet.tools import *
import random


class TestConversions(unittest.TestCase):

    def test_data(self):
        for i in range(100):
            word = random_word(30)
            self.assertEqual(word, bin_to_data(data_to_bin(word)))

    def test_int(self):
        for i in range(100):
            x = random.randint(0, 10000000)
            self.assertEqual(x, bin_to_int(int_to_bin(x)))

    def test_list_to_string(self):
        for i in range(100):
            word = random_word(30, string.digits)
            self.assertEqual(word, list_to_string(string_to_list(word)))


if __name__ == '__main__':
    unittest.main()
