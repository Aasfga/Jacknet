import numpy

import jacknet.pulseaudio as pa
import jacknet.pulseaudio.simple
from jacknet.devices.jack_device import JackDevice


class RealJack(JackDevice):
    def __init__(self, time):
        super().__init__(time)

    def _end(self):
        self.recorder.close()
        del self.recorder

    def _read(self, bits):
        return self.recorder.read(bits)

    def _start(self):
        self.recorder = pa.simple.open(direction=pa.STREAM_RECORD, format=pa.SAMPLE_S16LE,
                                                       rate=self.framerate, channels=1)

    def _write(self, data):
        writer = jacknet.pulseaudio.simple.open(direction=pa.STREAM_PLAYBACK, format=pa.SAMPLE_S16LE,
                                                rate=self.framerate, channels=1)
        writer.write(numpy.array(data) * (2**15))
        writer.drain()
        writer.close()
