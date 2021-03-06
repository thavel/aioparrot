from aioparrot.ardrone.utils import parrot_str


def move(progressive):
    """
    * left-right tilt (float): from -1 (left) to +1 (right).
    * front-back tilt (float): from -1 (forwards) to +1 (backwards).
    * vertical speed (float): from -1 (down) to +1 (up).
    * angular speed (float): from -1 (spin left) to +1 (spin right).
    + progressive (boolean): disable/enable (for hovering).
    """
    def wrapper(func):
        def call(*args, **kwargs):
            data = func(*args, **kwargs)
            data = [int(progressive)] + [float(value) for value in data]
            return args[0].format('PCMD', data)
        return call
    return wrapper


def action(func):
    """
    * flag (binary): 10 bits flag.
    """
    def call(*args, **kwargs):
        data = 0b10001010101000000000000000000
        data += func(*args, **kwargs)
        return args[0].format('REF', [data])
    return call


class CommandFactory(object):
    """
    ARDrone 1 and 2 controller.
    """
    def __init__(self):
        self._seq = 0

    @property
    def seq(self):
        self._seq += 1
        return self._seq

    def format(self, command, data):
        params = ['{}'] + [parrot_str(value) for value in data]
        return 'AT*{}={}\r'.format(command, ','.join(params))

    def altitude(self, meters):
        meters *= 1000
        return self.format('CONFIG', ['control:altitude_max', str(meters)])

    @action
    def takeoff(self):
        return 0b1000000000

    @action
    def land(self):
        return 0b0000000000

    def trim(self):
        return self.format('FTRIM', [])

    @move(progressive=False)
    def hover(self):
        return [0, 0, 0, 0]

    @move(progressive=True)
    def left(self, speed):
        return [-speed, 0, 0, 0]

    @move(progressive=True)
    def right(self, speed):
        return [speed, 0, 0, 0]

    @move(progressive=True)
    def forward(self, speed):
        return [0, -speed, 0, 0]

    @move(progressive=True)
    def backward(self, speed):
        return [0, speed, 0, 0]

    @move(progressive=True)
    def down(self, speed):
        return [0, 0, -speed, 0]

    @move(progressive=True)
    def up(self, speed):
        return [0, 0, speed, 0]

    @move(progressive=True)
    def turn_left(self, speed):
        return [0, 0, 0, -speed]

    @move(progressive=True)
    def turn_right(self, speed):
        return [0, 0, 0, speed]

    @action
    def emergency(self):
        return 0b0100000000

    def auto(self, start=True):
        return self.format('AFLIGHT', [int(start)])

    def ping(self):
        return self.format('COMWDG', [])
