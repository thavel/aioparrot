import asyncio
import logging
from signal import SIGINT

from aioparrot import Device, drone


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
client = None


def stop():
    asyncio.ensure_future(cancel(abort=True))

async def cancel(abort=False):
    global client
    if abort and client:
        log.info("Aborting the mission")
        await client.land()
        await client.stop()
    loop = asyncio.get_event_loop()
    loop.call_soon_threadsafe(loop.stop)

async def main():
    global client
    client = drone(Device.ARDRONE2)
    client.ceiling = 10
    client.speed = 0.2

    log.info("Launching the drone")
    await client.start()
    await client.takeoff()
    await client.forward(2)
    await client.land()
    await client.stop()
    log.info("Mission completed")
    await cancel()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(main())
    loop.add_signal_handler(SIGINT, stop)
    loop.run_forever()
    log.info("Exit")
