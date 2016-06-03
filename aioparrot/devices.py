from enum import IntEnum


class Device(IntEnum):
    ARDRONE1 = 0
    ARDRONE2 = 1
    BEBOP = 2
    AIRBORNE = 3
    JUMPING = 4

    @property
    def sdk(self):
        if self.value in (self.ARDRONE1, self.ARDRONE2):
            return 2
        return 3
