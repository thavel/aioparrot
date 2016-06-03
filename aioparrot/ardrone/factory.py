from aioparrot.ardrone.utils import parrot_str


def move(progressive):
    """
    * left-right tilt (float): from -1 (left) to +1 (right)
    * front-back tilt (float): from -1 (forwards) to +1 (backwards)
    * vertical speed (float): from -1 (down) to +1 (up)
    * angular speed (float): from -1 (spin left) to +1 (spin right)
    + progressive (boolean): disable/enable (for hovering)
    """
    def wrapper(func):
        def call(*args, **kwargs):
            data = func(*args, **kwargs)
            data = [int(progressive)] + [float(value) for value in data]
            return args[0].format('PCMD', data)
        return call
    return wrapper


class CommandFactory(object):
    """
    ARDrone 1 and 2 controller.
    """
    def __init__(self, speed=0.1):
        self.seq = 0
        self.speed = speed

    def format(self, command, data):
        self.seq += 1
        params = [str(self.seq)] + [parrot_str(value) for value in data]
        return 'AT*{}={}\r'.format(command, ','.join(params))

    def takeoff(self, *args, **kwargs):
        raise NotImplementedError

    def land(self, *args, **kwargs):
        raise NotImplementedError

    def trim(self, *args, **kwargs):
        raise NotImplementedError

    @move(progressive=False)
    def hover(self):
        return [0, 0, 0, 0]

    @move(progressive=True)
    def left(self, unit=1):
        return [-(self.speed * unit), 0, 0, 0]

    @move(progressive=True)
    def right(self, unit=1):
        return [self.speed * unit, 0, 0, 0]

    @move(progressive=True)
    def forward(self, unit=1):
        return [0, -(self.speed * unit), 0, 0]

    @move(progressive=True)
    def backward(self, unit=1):
        return [0, self.speed * unit, 0, 0]

    @move(progressive=True)
    def down(self, unit=1):
        return [0, 0, -(self.speed * unit), 0]

    @move(progressive=True)
    def up(self, unit=1):
        return [0, 0, self.speed * unit, 0]

    @move(progressive=True)
    def turn_left(self, unit=1):
        return [0, 0, 0, -(self.speed * unit)]

    @move(progressive=True)
    def turn_right(self, unit=1):
        return [0, 0, 0, self.speed * unit]

    def halt(self, *args, **kwargs):
        raise NotImplementedError
