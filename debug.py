import asyncio
import logging

from aioparrot import Device, drone
from aioparrot.ardrone.factory import CommandFactory


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


async def main():
    # factory = CommandFactory()
    # log.info("SDK version %s", Device.ARDRONE2.sdk)
    # log.info("Altitude: %s", factory.altitude(3000))
    # log.info("Hover: %s", factory.hover())
    # log.info("Left: %s", factory.left())
    # log.info("Right: %s", factory.right())
    # log.info("Forward: %s", factory.forward())
    # log.info("Backward: %s", factory.backward())
    # log.info("Down: %s", factory.down())
    # log.info("Up: %s", factory.up())
    # log.info("Turn left: %s", factory.turn_left())
    # log.info("Turn right: %s", factory.turn_right())
    # log.info("Takeoff: %s", factory.takeoff())
    # log.info("Land: %s", factory.land())
    # log.info("Trim: %s", factory.trim())
    # log.info("Auto on: %s", factory.auto())
    # log.info("Auto off: %s", factory.auto(False))
    # log.info("Ping: %s", factory.ping())

    client = drone(Device.ARDRONE2)
    client.ceiling = 10
    client.speed = 0.2

    await client.start()
    await client.takeoff()
    await asyncio.sleep(3)
    await client.land()
    await client.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main(), loop=loop)
    loop.run_forever()
