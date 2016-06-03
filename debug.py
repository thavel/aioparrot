import asyncio
import logging

from aioparrot import Device, Drone


log = logging.getLogger(__name__)


async def main():
    drone = Drone(Device.ARDRONE2)
    log.critical(drone.device.sdk)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
