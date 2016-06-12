import struct
import asyncio


class BoundedFuture(asyncio.Future):
    def __init__(self, duration, *, loop=None):
        super().__init__(loop=loop)
        self.deadline = self._loop.time() + duration


def floating_point(value):
    """
    Gives a signed integer value for a given IEEE-754 floating-point value.
    """
    return struct.unpack('i', struct.pack('f', value))[0]


def parrot_str(value):
    """
    Convert any value into a Parrot compatible format.
    """
    if isinstance(value, float):
        value = floating_point(value)
    if isinstance(value, str):
        value = '"{}"'.format(value)
    return str(value)


class Options:

    def __init__(self):
        self._speed = 0.2
        self._ceiling = 5

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if value > 1:
            raise ValueError("Speed can't exceed 1")
        self._speed = value

    @property
    def ceiling(self):
        return self._ceiling

    @ceiling.setter
    def ceiling(self, value):
        if value > 1000:
            raise ValueError("Max altitude can't exceed 1km")
        self._ceiling = value
