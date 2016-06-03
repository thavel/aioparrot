import asyncio
import logging

from aioparrot import Device, Drone
from aioparrot.ardrone.factory import CommandFactory


log = logging.getLogger(__name__)


async def main():
    drone = Drone(Device.ARDRONE2)
    log.critical("SDK version %s", drone.device.sdk)

    factory = CommandFactory()
    log.critical("Altitude: %s", factory.altitude(3000))
    log.critical("Hover: %s", factory.hover())
    log.critical("Left: %s", factory.left())
    log.critical("Right: %s", factory.right())
    log.critical("Forward: %s", factory.forward())
    log.critical("Backward: %s", factory.backward())
    log.critical("Down: %s", factory.down())
    log.critical("Up: %s", factory.up())
    log.critical("Turn left: %s", factory.turn_left())
    log.critical("Turn right: %s", factory.turn_right())
    log.critical("Takeoff: %s", factory.takeoff())
    log.critical("Land: %s", factory.land())
    log.critical("Trim: %s", factory.trim())
    log.critical("Auto on: %s", factory.auto())
    log.critical("Auto off: %s", factory.auto(False))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
