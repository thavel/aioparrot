import asyncio
import logging

from aioparrot import Device, drone


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


async def main():
    client = drone(Device.ARDRONE2)
    client.ceiling = 10
    client.speed = 0.2

    await client.start()
    await client.takeoff()
    await client.left(2)
    await client.right(2)
    await client.land()
    await client.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main(), loop=loop)
    loop.run_forever()
