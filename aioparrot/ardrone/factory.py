class CommandFactory(object):
    """
    ARDrone 1 and 2 controller.
    """
    async def takeoff(self, *args, **kwargs):
        raise NotImplementedError

    async def land(self, *args, **kwargs):
        raise NotImplementedError

    async def trim(self, *args, **kwargs):
        raise NotImplementedError

    async def left(self, *args, **kwargs):
        raise NotImplementedError

    async def right(self, *args, **kwargs):
        raise NotImplementedError

    async def forward(self, *args, **kwargs):
        raise NotImplementedError

    async def backward(self, *args, **kwargs):
        raise NotImplementedError

    async def halt(self, *args, **kwargs):
        raise NotImplementedError

    async def up(self, *args, **kwargs):
        raise NotImplementedError

    async def down(self, *args, **kwargs):
        raise NotImplementedError

    async def turn_left(self, *args, **kwargs):
        raise NotImplementedError

    async def turn_right(self, *args, **kwargs):
        raise NotImplementedError
