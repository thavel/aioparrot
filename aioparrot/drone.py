from aioparrot.devices import Device
from aioparrot.errors import DroneConfigError


class Drone(object):
    """
    Generic interface to handle any drone device.
    """
    def __init__(self, device):
        if device not in Device:
            raise DroneConfigError("Invalid Parrot device {}".format(device))
        self.device = device
