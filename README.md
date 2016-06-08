# aioparrot

[![Circle CI](https://img.shields.io/circleci/project/thavel/aioparrot/master.svg)](https://circleci.com/gh/thavel/aioparrot)

Asyncio (PEP-3156) based project to control Parrot drones.


## Compatibility

Currently supported devices:
* AR Drone 1 and 2 (SDK 2)

Upcoming support:
* Bebop Drone, Airborne Drone and Jumping Drone (SDK 3)


## Credits

* [venthur](https://github.com/venthur)/[python-ardrone](https://github.com/venthur/python-ardrone)


## ARDrone client API

```python
client = drone(Device.ARDRONE2)
await client.start()
await client.takeoff()
await client.left()
await client.land()
await client.stop()
```
