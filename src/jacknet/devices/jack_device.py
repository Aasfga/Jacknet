from jacknet.devices.abstract_device import AbstractDevice
import numpy as np
from numpy.fft import fft
from jacknet.tools import *


class JackDevice(AbstractDevice):
    framerate = 1 * 44100
    ZERO = 440
    ONE = 880

    @staticmethod
    def ceil(x):
        if int(x + 1) == x + 1:
            return int(x)
        else:
            return int(x + 1)

    @staticmethod
    def create_signal(fq, t):
        fr = JackDevice.framerate
        pi = np.pi
        n = int(fr * t)
        t = np.linspace(0.0, t, n)
        return list(np.sin(t * fq * 2 * pi))

    def one(self):
        return int(self.ONE * self.time)

    def zero(self):
        return int(self.ZERO * self.time)

    def __init__(self, time):
        self.time = time

    def _start(self):
        raise NotImplementedError

    def _end(self):
        raise NotImplementedError

    def _read(self, bits):
        raise NotImplementedError


    def _write(self, data):
        raise NotImplementedError

    def _convert_signal(self, signal):
        fft_list = fft(signal)
        fft_list = fft_list[:len(fft_list)//2]
        x = np.abs(np.argmax(np.abs(fft_list)))
        if abs(x - self.zero()) < 5:
            return 0
        elif abs(x - self.one()) < 5:
            return 1
        else:
            raise ValueError

    def _read_signal(self):
        return self._convert_signal(self._read(int(self.framerate * self.time)))

    def _read_data(self, n):
        data = []
        n = (n//4)*5
        for i in range(n):
            data.append(self._read_signal())
        return data

    @staticmethod
    def get_max(fft_list, x):
        pointer = x
        for i in range(x-2, x+2):
            if np.abs(fft_list[pointer]) < np.abs(fft_list[i]):
                pointer = i
        return pointer

    def _is_synchronized(self):
        signal = self._read(int(self.framerate * self.time))
        fft_list = fft(signal)[:1000]
        fft_list[0] = 0
        zero_p = self.get_max(fft_list, self.zero())
        one_p = self.get_max(fft_list, self.one())
        zero = np.abs(fft_list[zero_p])
        one = np.abs(fft_list[one_p])
        fft_list[one_p] = 0
        fft_list[zero_p] = 0
        zero_list = [np.abs(x) for x in fft_list if abs(x) > 0.3 * zero]
        one_list = [np.abs(x) for x in fft_list if abs(x) > 0.3 * one]
        return len(zero_list) == 0 or len(one_list) == 0

    def _move_cursor(self):
        self._read(int(self.framerate * self.time * 0.05))

    def _is_preamble(self):
        byte = self._read_data(8)
        i = byte[0]

        for x in byte:
            if i != x:
                return False
            i = 1 - i
        return True

    def _read_preamble(self):
        crr = 0
        last = 0
        while crr != 1 or last != 1:
            last = crr
            crr = self._read_signal()

    def get_msg(self):
        self._start()
        while True:
            while not self._is_synchronized():
                self._move_cursor()
            try:
                if self._is_preamble():
                    break
            except ValueError:
                continue
        self._read_preamble()
        first, second = list_to_string(self._read_data(6 * 8)), list_to_string(self._read_data(6 * 8))
        length = list_to_string(self._read_data(4 * 8))
        l = bin_to_int(self.conv5b4b(length))
        data = list_to_string(self._read_data(l * 8))
        crc = list_to_string(self._read_data(4 * 8))
        self._end()
        return self.conv5b4b(first + second + length + data + crc)

    def _preamble(self):
        return "10101010" * 7 + "10101011"

    def send_msg(self, data):
        one = self.create_signal(self.ONE, self.time)
        zero = self.create_signal(self.ZERO, self.time)
        data = self._preamble() + self.conv4b5b(data)
        res = []
        for x in data:
            if x == "0":
                res += self.create_signal(self.ZERO, self.time)
            else:
                res += self.create_signal(self.ONE, self.time)
        self._write(res)
