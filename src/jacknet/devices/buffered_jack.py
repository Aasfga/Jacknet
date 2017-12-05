from jacknet.devices.jack_device import JackDevice
import random

class BufferedJack(JackDevice):

    def _create_noise(self):
        noise = []

        for i in range(1000):
            wave = self.create_signal(random.choice([220, 330, 440, 550, 660, 770, 880]), random.uniform(0, 0.1))
            noise += wave
        return noise


    def __init__(self, time):
        super().__init__(time)
        self.buffer = self._create_noise()
        self.iter = 0

    def _read(self, bits):
        res = self.buffer[self.iter:self.iter + bits]
        self.iter += bits
        if self.iter == len(self.buffer):
            self.iter = 0
            self.buffer = self._create_noise()
        return res

    def _write(self, data):
        self.buffer += data

    def _end(self):
        pass

    def _start(self):
        pass
