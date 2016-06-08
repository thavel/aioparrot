from aioparrot.devices import Device
from aioparrot.errors import DroneConfigError
from aioparrot.ardrone import Client as ARDroneClient


MAPPING = {
    Device.ARDRONE1: ARDroneClient,
    Device.ARDRONE2: ARDroneClient,
    Device.BEBOP: None,
    Device.AIRBORNE: None,
    Device.JUMPING: None
}


def drone(device):
    if device not in Device:
        raise DroneConfigError("Invalid Parrot device {}".format(device))

    client = MAPPING[device]
    if not client:
        raise NotImplementedError("Drone client hasn't been implemented yet")

    return client()
