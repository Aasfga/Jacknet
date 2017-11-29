# vim:ts=4:sts=4:sw=4:expandtab

import ctypes
import os
import wave

import jacknet.pulseaudio.defs as defs
import numpy as np

import jacknet.pulseaudio.types as types

#TODO: safeguard 
library = ctypes.cdll.LoadLibrary('libpulse-simple.so.0')

library.pa_strerror.argtypes           = [ ctypes.c_int ]
library.pa_strerror.restype            = ctypes.c_char_p 
library.pa_simple_new.argtypes         = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.POINTER(
    types.pa_sample_spec), ctypes.POINTER(types.pa_channel_map), ctypes.POINTER(types.pa_buffer_attr), ctypes.POINTER(ctypes.c_int)]
library.pa_simple_new.restype          = ctypes.c_void_p
library.pa_simple_read.argtypes        = [ ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_int) ]
library.pa_simple_read.restype         = ctypes.c_int
library.pa_simple_write.argtypes       = [ ctypes.c_void_p, ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_int) ]
library.pa_simple_write.restype        = ctypes.c_int
library.pa_simple_drain.argtypes       = [ ctypes.c_void_p, ctypes.POINTER(ctypes.c_int) ]
library.pa_simple_drain.restype        = ctypes.c_int
library.pa_simple_flush.argtypes       = [ ctypes.c_void_p, ctypes.POINTER(ctypes.c_int) ]
library.pa_simple_flush.restype        = ctypes.c_int
library.pa_simple_get_latency.argtypes = [ ctypes.c_void_p, ctypes.POINTER(ctypes.c_int) ]
library.pa_simple_get_latency.restype  = ctypes.c_ulonglong
library.pa_simple_free.argtypes        = [ ctypes.c_void_p ]
library.pa_simple_free.restype         = None

pa_strerror = library.pa_strerror
pa_simple_free = library.pa_simple_free
def safe_pa_call(fun):
    def inner(*args):
        error = ctypes.c_int(0)
        args = list(args)
        args.append(ctypes.pointer(error))
        ret = fun(*args)
        if error.value != 0:
            strerror = pa_strerror(error)
            raise IOError(strerror)
        return ret
    return inner
pa_simple_new         = safe_pa_call(library.pa_simple_new)
pa_simple_read        = safe_pa_call(library.pa_simple_read)
pa_simple_write       = safe_pa_call(library.pa_simple_write)
pa_simple_drain       = safe_pa_call(library.pa_simple_drain)
pa_simple_flush       = safe_pa_call(library.pa_simple_flush)
pa_simple_get_latency = safe_pa_call(library.pa_simple_get_latency)

class SimpleConnection(object):
    def __init__(self, connection, sample_spec, channel_map, buffer_attr):
        self.connection = connection
        self.sample_spec = sample_spec
        self.channel_map = channel_map
        self.buffer_attr = buffer_attr

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def read_raw(self, size):
        if self.connection is None:
            raise IOError("Closed connection")
        data = b'\x00' * size
        pa_simple_read(self.connection, data, size)
        return data

    def write_raw(self, data):
        if self.connection is None:
            raise IOError("Closed connection")
        pa_simple_write(self.connection, data, len(data))

    def read(self, nsamples):
        if self.connection is None:
            raise IOError("Closed connection")
        sample_len = self.sample_width
        sample_typ = defs.SAMPLE_TYPE[self.format]
                
        samples_raw = self.read_raw(nsamples*sample_len*self.channels)
        samples = np.fromstring(samples_raw, dtype=sample_typ).astype(np.float)
        return samples

    def write(self, samples):
        if self.connection is None:
            raise IOError("Closed connection")
        sample_len = self.sample_width
        sample_typ = defs.SAMPLE_TYPE[self.format]
        samples = np.array(samples).astype(sample_typ).tostring()
        return self.write_raw(samples)

    def drain(self):
        if self.connection is None:
            raise IOError("Closed connection")
        pa_simple_drain(self.connection)

    def flush(self):
        if self.connection is None:
            raise IOError("Closed connection")
        pa_simple_flush(self.connection)

    def close(self):
        if self.connection is not None:
            pa_simple_free(self.connection)
            self.connection = None

    @property
    def latency(self):
        if self.connection is None:
            raise IOError("Closed connection")
        return pa_simple_get_latency(self.connection)

    @property
    def format(self):
        if self.connection is None:
            raise IOError("Closed connection")
        return self.sample_spec.format

    @property
    def sample_width(self):
        if self.connection is None:
            raise IOError("Closed connection")
        return defs.SAMPLE_WIDTH[self.format]

    @property
    def sample_type(self):
        if self.connection is None:
            raise IOError("Closed connection")
        return defs.SAMPLE_TYPE[self.format]

    @property
    def rate(self):
        if self.connection is None:
            raise IOError("Closed connection")
        return self.sample_spec.rate

    @property
    def channels(self):
        if self.connection is None:
            raise IOError("Closed connection")
        return self.sample_spec.channels

class WaveConnection(SimpleConnection):

    def read_raw(self, size):
        if self.connection is None:
            raise IOError("Closed connection")
        data = self.connection.readframes(size//self.sample_width)
        res = bytes(bytearray(data))
        res += b'\x00'*(size - len(res))
        return res

    def write_raw(self, data):
        if self.connection is None:
            raise IOError("Closed connection")
        self.connection.writeframes(data)

    def drain(self):
        if self.connection is None:
            raise IOError("Closed connection")
        pass

    def flush(self):
        if self.connection is None:
            raise IOError("Closed connection")
        pass

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

def open(direction, format, rate, channels, name=None, stream_name=None, server=None, device=None):
    if name is None:
        name = 'python'
    if stream_name is None:
        stream_name = 'python'

    if name is not None and isinstance(name, str):
        name = bytes(name, 'utf8')
    if stream_name is not None and isinstance(stream_name, str):
        stream_name = bytes(stream_name, 'utf8')
    if server is not None and isinstance(server, str):
        server = bytes(server, 'utf8')
    if device is not None and isinstance(device, str):
        device = bytes(device, 'utf8')

    ss = types.pa_sample_spec()
    ss.format = format
    ss.rate = rate
    ss.channels = channels

#TODO: allow use of cm
    #cm = types.pa_channel_map()
    cm = None

#TODO: allow use of ba
    #ba = types.pa_buffer_attr()
    ba = None

    wavfile =  os.environ.get('__PULSEAUDIO_WAVFILE__', None)
    if wavfile is not None:
        wavmode = 'wb'
        if direction == defs.STREAM_RECORD:
            wavmode = 'rb'
        connection = wave.open(wavfile, wavmode)
        if direction == defs.STREAM_RECORD:
            guess = {
                1 : defs.SAMPLE_U8,
                2 : defs.SAMPLE_S16LE,
                3 : defs.SAMPLE_S24LE,
                4 : defs.SAMPLE_S32LE,
            }
            ss.format = guess[connection.getsampwidth()]
            ss.rate = connection.getframerate()
            ss.channels = connection.getnchannels()
        else:
            connection.setnchannels(channels)
            connection.setsampwidth(defs.SAMPLE_WIDTH[format])
            connection.setframerate(rate)
        return WaveConnection(connection, ss, cm, ba)
    else:
        connection = pa_simple_new(server, name, direction, device, stream_name, ctypes.pointer(ss) if ss is not None else None, ctypes.pointer(cm) if cm is not None else None, ctypes.pointer(ba) if ba is not None else None)
        return SimpleConnection(connection, ss, cm, ba)
