import math
from djitellopy import tello
from enum import Enum, IntEnum, StrEnum


class DIRECTION(StrEnum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    FORWARD = "forward"
    BACK = "back"

class ROTATION_DIRECTION(Enum):
    CLOCKWISE = 0
    COUNTERCLOCKWISE = 1

class SPEED(IntEnum):
    SLOW = 10
    MEDIUM = 25
    FAST = 45

class Drone:
    def __init__(self):
        self.drone = tello.Tello()

    def connect(self):
        # TODO Log action

        self.drone.connect()

    def reboot(self):
        # TODO Log action

        self.drone.reboot()

    def takeoff(self):
        # TODO Log action

        self.drone.takeoff()
    
    def land(self):
        # TODO Log action

        self.drone.land()
    
    def startStream(self):
        # TODO Log action

        self.drone.streamon()

    def stopStream(self):
        # TODO Log action

        self.drone.streamoff()

    def emergency(self):
        # TODO Log action

        self.drone.emergency()

    def move(self, dir: DIRECTION, x: int):
        """Fly x cm in direction dir."""
        # TODO Log action

        self.drone.move(dir, x)

    def moveToXYZRelativeToCurrentPosition(self, x: int, y: int, z: int, speed: SPEED):
        #TODO Log action

        self.drone.go_xyz_speed(x, y, z, speed)

    def moveToXYZRelativeToPad(self, x: int, y: int, z: int, speed: SPEED, pad: int):
        # TODO Log action

        self.drone.go_xyz_speed_mid(x, y, z, speed, pad)

    def rotate(self, dir: ROTATION_DIRECTION, angle_deg: int):
        # TODO Log action

        if dir is ROTATION_DIRECTION.CLOCKWISE:
            self.drone.rotate_clockwise(angle_deg)
        elif dir is ROTATION_DIRECTION.COUNTERCLOCKWISE:
            self.drone.rotate_counter_clockwise(angle_deg)

    def circleObject(self, radius_cm: int, speed: SPEED, steps: int = 24):
        """Circles around the object 
        
        Steps size dictates the circle smoothness
        """
        for i in range(steps):
            angle = 2 * math.pi * i / steps                                                                                                                                  
            next_angle = 2 * math.pi * (i + 1) / steps                                                                                                                       
            x = round(radius_cm * (math.cos(next_angle) - math.cos(angle)))
            y = round(radius_cm * (math.sin(next_angle) - math.sin(angle)))                                                                                                    
            self.moveToXYZRelativeToCurrentPosition(x, y, 0, speed)
            self.rotate(ROTATION_DIRECTION.CLOCKWISE, 360 // steps)        

    def startSequence(self):
        # TODO
        pass

    def setSpeed(self, speed: SPEED):
        # TODO Log action

        self.drone.set_speed(speed)


    def getBattery(self):
        # TODO Log action

        return self.drone.get_battery()
    
    def getFrame(self):
        return self.drone.get_frame_read()

            
