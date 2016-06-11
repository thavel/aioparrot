import asyncio
import logging
from enum import IntEnum

from aioparrot.ardrone.factory import CommandFactory
from aioparrot.ardrone.utils import Options


log = logging.getLogger(__name__)


def move(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class Port(IntEnum):
    NAVDATA = 5554
    VIDEO = 5555
    COMMAND = 5556


class _Protocol(object):

    WATCHDOG = 1.0

    def __init__(self, loop, opt):
        self.loop = loop
        self._transport = None
        self._timer = None
        self._ceiling = 5000
        self._factory = CommandFactory()
        self._options = opt

    @property
    def duration(self):
        return asyncio.sleep(self._options.speed * 20)

    def connection_made(self, transport):
        self._transport = transport
        self._start_timer()

    def connection_lost(self, exc):
        if self._timer:
            self._timer.cancel()
        log.debug("Command stream closed")

    def datagram_received(self, data, addr):
        data = data.decode()
        log.debug("Command stream received: %s", data)

    def error_received(self, exc):
        log.error("Command stream received an error: %s", str(exc))

    def send(self, data):
        if self._timer:
            self._timer.cancel()
        if not self._transport:
            log.error("Command stream can't send: %s", data)
            return
        self._transport.sendto(data.encode())
        log.debug("Command stream sent: %s", data)
        self._start_timer()

    def _start_timer(self):
        when = self.loop.time() + self.WATCHDOG
        self._timer = self.loop.call_at(when, self._ping)

    def _ping(self):
        data = self._factory.ping()
        self.send(data)

    def altitude(self, value):
        data = self._factory.altitude(value)
        self.send(data)

    def trim(self):
        data = self._factory.trim()
        self.send(data)

    def panic(self):
        data = self._factory.emergency()
        self.send(data)

    def auto(self, start=True):
        data = self._factory.auto(start)
        self.send(data)

    async def halt(self):
        data = self._factory.emergency()
        self.send(data)

    async def takeoff(self):
        self.trim()
        self.altitude(self._options.ceiling)
        data = self._factory.takeoff()
        self.send(data)
        await self.duration

    async def land(self):
        data = self._factory.land()
        self.send(data)
        await self.duration

    @move
    async def hover(self):
        data = self._factory.hover()
        self.send(data)
        await self.duration

    @move
    async def left(self, unit=1):
        data = self._factory.left(self._options.speed)
        self.send(data)
        await self.duration

    @move
    async def right(self, unit=1):
        data = self._factory.right(self._options.speed)
        self.send(data)
        await self.duration

    @move
    async def forward(self, unit=1):
        data = self._factory.forward(self._options.speed)
        self.send(data)
        await self.duration

    @move
    async def backward(self, unit=1):
        data = self._factory.backward(self._options.speed)
        self.send(data)
        await self.duration

    @move
    async def down(self, unit=1):
        data = self._factory.down(self._options.speed)
        self.send(data)
        await self.duration

    @move
    async def up(self, unit=1):
        data = self._factory.up(self._options.speed)
        self.send(data)
        await self.duration

    @move
    async def turn_left(self, unit=1):
        data = self._factory.left(self._options.speed)
        self.send(data)
        await self.duration

    @move
    async def turn_right(self, unit=1):
        data = self._factory.left(self._options.speed)
        self.send(data)
        await self.duration


class Client(asyncio.Future):

    DRONE_ADDR = '192.168.1.1'

    def __init__(self, *, loop=None):
        super().__init__(loop=loop)
        self._transport = None
        self._protocol = None
        self._options = Options()

    @property
    def transport(self):
        return self._transport

    @property
    def protocol(self):
        return self._protocol

    @property
    def speed(self):
        return self._options.speed

    @property
    def ceiling(self):
        return self._options.ceiling

    @speed.setter
    def speed(self, value):
        self._options.speed = value

    @ceiling.setter
    def ceiling(self, value):
        self._options.ceiling = value
        if self._protocol:
            self._protocol.altitude(self._options.ceiling)

    async def start(self):
        future = self._loop.create_datagram_endpoint(
            lambda: _Protocol(self._loop, self._options),
            remote_addr=(self.DRONE_ADDR, Port.COMMAND.value)
        )
        self._transport, self._protocol = await future

    async def stop(self):
        await self._protocol.halt()
        self._transport.close()

    def __getattribute__(self, name):
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return getattr(self._protocol, name)
