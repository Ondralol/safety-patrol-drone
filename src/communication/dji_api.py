import math
from djitellopy import tello
from enum import Enum, IntEnum, StrEnum
import threading

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

    def _run(self, fn, *args):
        """Runs function in another thread"""

        # Only one thread can be running at the same time
        if hasattr(self, '_worker') and self._worker.is_alive():
            return  # ignore if command already running

        self._worker = threading.Thread(target=fn, args=args, daemon=True)
        self._worker.start()


    def connect(self):
        self._run(self.drone.connect)

    def end(self):
        self._run(self.drone.end())


    def reboot(self):
        self._run(self.drone.reboot)


    def takeoff(self):
        self._run(self.drone.takeoff)
    

    def land(self):
        self._run(self.drone.land)


    def startStream(self):
        self._run(self.drone.streamon)


    def stopStream(self):
        self._run(self.drone.streamoff)


    def emergency(self):
        self._run(self.drone.emergency)


    def enableMissionPads(self):
        self._run(self.drone.enable_mission_pads)


    def move(self, dir: DIRECTION, x: int):
        """Fly x cm in direction dir."""

        self._run(lambda: self.drone.move(dir, x))


    def moveToXYZRelativeToCurrentPosition(self, x: int, y: int, z: int, speed: SPEED):
        self._run(lambda: self.drone.go_xyz_speed(x, y, z, speed))


    def moveToXYZRelativeToPad(self, x: int, y: int, z: int, speed: SPEED, pad: int):
        self._run(lambda: self.drone.go_xyz_speed_mid(x, y, z, speed, pad))


    def rotate(self, dir: ROTATION_DIRECTION, angle_deg: int):
        if dir is ROTATION_DIRECTION.CLOCKWISE:
            self._run(lambda: self.drone.rotate_clockwise(angle_deg))
        elif dir is ROTATION_DIRECTION.COUNTERCLOCKWISE:
            self._run(lambda: self.drone.rotate_counter_clockwise(angle_deg))


    def circleObject(self, radius_cm: int, speed: SPEED, steps: int = 24):
        """Circles around the object 
        
        Steps size dictates the circle smoothness
        """

        # Needs to be wrapped in order to be able to call in in a thread
        def _circle():
            for i in range(steps):
                angle = 2 * math.pi * i / steps                                                                                                                                  
                next_angle = 2 * math.pi * (i + 1) / steps                                                                                                                       
                x = round(radius_cm * (math.cos(next_angle) - math.cos(angle)))
                y = round(radius_cm * (math.sin(next_angle) - math.sin(angle)))                                                                                                    
                self.drone.go_xyz_speed(x, y, 0, speed)
                self.drone.rotate_clockwise(360 // steps)       
        self._run(_circle)    


    def startSequence(self):
        """Automatic sequence on predefined path"""
        pass


    def setSpeed(self, speed: SPEED):
        self._run(lambda: self.drone.set_speed(speed))


    def getBattery(self):
        try:
            return self.drone.get_battery()
        except:
            return None
        

    def getHeight(self):
        try:
            return self.drone.get_height()
        except:
            return None
        

    def getDistanceTof(self):
        "Another measurement for height"
        try:
            return self.drone.get_distance_tof()
        except:
            return None

    

    def getMissionpadXYZ(self):
        try:
            x = self.drone.get_mission_pad_distance_x()
            y = self.get_mission_pad_distance_y()
            z = self.get_mission_pad_distance_z()

            return x, y, z
        except:
            return None
    

    def getFrame(self):
        try:
            return self.drone.get_frame_read()
        except:
            return None

            
