# vim:ts=4:sts=4:sw=4:expandtab

import ctypes

import jacknet.pulseaudio.defs as defs


###
#  pa_sample_spec
###
class pa_sample_spec(ctypes.Structure):
    __slots__ = ['format', 'rate', 'channels',]
pa_sample_spec._fields_ = [
    ('format', ctypes.c_int),
    ('rate', ctypes.c_uint32),
    ('channels', ctypes.c_uint8),
]
###
#  pa_channel_map
###
class pa_channel_map(ctypes.Structure):
    __slots__ = ['channels', 'map',]
pa_channel_map._fields_ = [
    ('channels', ctypes.c_uint8),
    ('map', ctypes.c_int * defs.CHANNELS_MAX),
]
###
#  pa_buffer_attr
###
class pa_buffer_attr(ctypes.Structure):
    __slots__ = ['maxlength', 'tlength', 'prebuf', 'minreq', 'fragsize',]
pa_buffer_attr._fields_ = [
    ('maxlength', ctypes.c_uint32),
    ('tlength', ctypes.c_uint32),
    ('prebuf', ctypes.c_uint32),
    ('minreq', ctypes.c_uint32),
    ('fragsize', ctypes.c_uint32),
]

