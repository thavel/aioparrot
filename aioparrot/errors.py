class DroneError(Exception):
    """
    Generic error.
    """
    pass


class DroneConfigError(DroneError):
    """
    Error while setting up the drone.
    """
    pass
