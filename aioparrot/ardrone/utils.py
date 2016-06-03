import struct


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
