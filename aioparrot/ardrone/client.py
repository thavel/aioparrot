import asyncio
import logging
from enum import IntEnum

from aioparrot.ardrone.factory import CommandFactory
from aioparrot.ardrone.utils import Options, BoundedFuture


log = logging.getLogger(__name__)


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
        self._move_duration = None

        self._factory = CommandFactory()
        self._options = opt

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

    def send(self, data, until=None):
        # Beforehand
        if self._timer:
            self._timer.cancel()
        data_seq = data.format(self._factory.seq)

        # Stop condition
        if not self._transport:
            log.error("Command stream can't send: %s", data_seq)
            return

        # Data sending
        self._transport.sendto(data_seq.encode())
        log.debug("Command stream sent: %s", data_seq)

        # Schedule next data sending
        if until:
            if not isinstance(until, BoundedFuture):
                until = BoundedFuture(until)
            if self.loop.time() <= until.deadline:
                # Schedule next call
                self._start_timer(self.send, data, until)
            else:
                # End the future and resume periodic ping
                until.set_result(None)
                self._start_timer()
        else:
            # Next periodic ping
            self._start_timer()

        # None or awaitable future
        return until

    def _start_timer(self, callback=None, *args, **kwargs):
        """
        Schedule a callback after the value (in seconds) of the watchdog.
        Default behavior: send a ping.
        """
        cb = (lambda: callback(*args, **kwargs)) if callback else self._ping
        when = self.loop.time() + self.WATCHDOG
        self._timer = self.loop.call_at(when, cb)

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
        await asyncio.sleep(1)

    async def takeoff(self):
        self.trim()
        self.altitude(self._options.ceiling)
        data = self._factory.takeoff()
        self.send(data)
        await asyncio.sleep(5)

    async def land(self):
        data = self._factory.land()
        self.send(data)
        await asyncio.sleep(3)
    
    async def hover(self, duration=1):
        data = self._factory.hover()
        await self.send(data, duration)

    async def left(self, duration=1):
        data = self._factory.left(self._options.speed)
        await self.send(data, duration)
    
    async def right(self, duration=1):
        data = self._factory.right(self._options.speed)
        await self.send(data, duration)
    
    async def forward(self, duration=1):
        data = self._factory.forward(self._options.speed)
        await self.send(data, duration)
    
    async def backward(self, duration=1):
        data = self._factory.backward(self._options.speed)
        await self.send(data, duration)
    
    async def down(self, duration=1):
        data = self._factory.down(self._options.speed)
        await self.send(data, duration)
    
    async def up(self, duration=1):
        data = self._factory.up(self._options.speed)
        await self.send(data, duration)
    
    async def turn_left(self, duration=1):
        data = self._factory.turn_left(self._options.speed)
        await self.send(data, duration)
    
    async def turn_right(self, duration=1):
        data = self._factory.turn_right(self._options.speed)
        await self.send(data, duration)


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
