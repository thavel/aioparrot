import asyncio
import logging
from enum import IntEnum

from aioparrot.ardrone.factory import CommandFactory


log = logging.getLogger(__name__)


class Port(IntEnum):
    NAVDATA = 5554
    VIDEO = 5555
    COMMAND = 5556


class _Protocol(object):

    WATCHDOG = 1.0

    def __init__(self, loop):
        self.loop = loop
        self._transport = None
        self._factory = CommandFactory()
        self._timer = None

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
        self._timer = self.loop.call_at(when, self.ping)

    def ping(self):
        data = self._factory.ping()
        self.send(data)

    async def halt(self):
        data = self._factory.emergency()
        self.send(data)


class Client(object):

    DRONE_ADDR = '192.168.1.1'

    def __init__(self, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.transport = None
        self.protocol = None

    async def start(self):
        future = self.loop.create_datagram_endpoint(
            lambda: _Protocol(self.loop),
            remote_addr=(self.DRONE_ADDR, Port.COMMAND.value)
        )
        self.transport, self.protocol = await future

    async def stop(self):
        await self.protocol.halt()
        self.transport.close()
