import math
from djitellopy import tello, Tello
from enum import Enum, IntEnum, StrEnum
import threading
import time

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


TIMEOUT = 5.0


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
        self._run(self.drone.end)


    def reboot(self):
        self._run(self.drone.reboot)

    def setBitRate(self):
        self._run(lambda: self.drone.set_video_bitrate(Tello.BITRATE_1MBPS))

    def takeoff(self):
        self._run(self.drone.takeoff)
    
    def keepAlive(self):
        try:                                                                                                                                          
          self.drone.send_command_without_return("command")
        except:                                                                                                                                       
          pass  

    def land(self):
        self._run(self.drone.land)


    def startStream(self):
        self._run(self.drone.streamon)


    def stopStream(self):
        self._run(self.drone.streamoff)


    def emergency(self):
        # Run instantly, not in a thread
        self.drone.emergency()


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


    def _buildInspectSequence(self):
            return [
            # Moving to left side
            lambda: self.drone.rotate_counter_clockwise(45),
            lambda: self.drone.move("forward", 25),
            lambda: self.drone.rotate_clockwise(90),
            lambda: self.drone.move("left", 50),

            # Go back to the starting point
            lambda: self.drone.move("right", 50),
            lambda: self.drone.rotate_counter_clockwise(90),
            lambda: self.drone.move("back", 20),
            lambda: self.drone.rotate_clockwise(45),

            # Moving to right side
            lambda: self.drone.rotate_clockwise(45),
            lambda: self.drone.move("forward", 25),
            lambda: self.drone.rotate_counter_clockwise(90),
            lambda: self.drone.move("right", 50),

            # Go back to the starting point
            lambda: self.drone.move("left", 50),
            lambda: self.drone.rotate_clockwise(90),
            lambda: self.drone.move("back", 20),
            lambda: self.drone.rotate_counter_clockwise(45),

        ]
    


    def inspectObject(self, on_done = None):
        """Inspect an object by sweeping left then right.

       """
        def _run_sequence():
            for step in self._buildInspectSequence():
                step()
                time.sleep(TIMEOUT)
            if on_done is not None:
                on_done()
                
        self._run(_run_sequence)


    def _build_sequence(self):
        # Drone starts in center facing forward
        return [
            # Go to front-left corner
            lambda: self.drone.move("left", 50),
            lambda: self.drone.move("forward", 50),

            # Turn right, go to front-right corner
            lambda: self.drone.rotate_clockwise(90),
            lambda: self.drone.move("forward", 100),

            # Turn right, go to back-right corner
            lambda: self.drone.rotate_clockwise(90),
            lambda: self.drone.move("forward", 100),

            # Turn right, go to back-left corner
            lambda: self.drone.rotate_clockwise(90),
            lambda: self.drone.move("forward", 100),

            # Turn right, go to front-left corner
            lambda: self.drone.rotate_clockwise(90),
            lambda: self.drone.move("forward", 100),

            # Return to center
            lambda: self.drone.rotate_clockwise(90),
            lambda: self.drone.move("forward", 50),
            lambda: self.drone.rotate_clockwise(90),
            lambda: self.drone.move("forward", 50),

            # Rotate back
            lambda: self.drone.rotate_clockwise(180)
        ]
    
    def _routineInspection(self):
            return [
            # Moving to top left corner
            lambda: self.drone.rotate_counter_clockwise(45),
            lambda: self.drone.move("forward", 100),
            lambda: self.drone.rotate_clockwise(135),

            # Moving in a square around grid  
            lambda: self.drone.move("forward", 150),
            lambda: self.drone.rotate_clockwise(90),
            lambda: self.drone.move("forward", 150),
            lambda: self.drone.rotate_clockwise(90),
            lambda: self.drone.move("forward", 150),
            lambda: self.drone.rotate_clockwise(90),
            lambda: self.drone.move("forward", 150),
            lambda: self.drone.rotate_clockwise(135),

            # Moving in a diagonal around grid  
            lambda: self.drone.move("forward", 200),
            lambda: self.drone.rotate_clockwise(135),
            lambda: self.drone.move("forward", 150),
            lambda: self.drone.rotate_clockwise(135),
            lambda: self.drone.move("forward", 200),
            lambda: self.drone.rotate_clockwise(180),
            lambda: self.drone.move("forward", 100),
        ]

    def startSequence(self):
        """Fly predefined perimeter path."""
        def _run_sequence():
            for step in self._routineInspection():
                step()
        self._run(_run_sequence)

    def setSpeed(self, speed: SPEED):
        self._run(lambda: self.drone.set_speed(speed))


    def getBattery(self):
        try:
            return self.drone.get_battery()
        except:
            return None
        
    def getTemp(self):
        try:
            return self.drone.get_temperature()
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
            y = self.drone.get_mission_pad_distance_y()
            z = self.drone.get_mission_pad_distance_z()

            return x, y, z
        except:
            return None
    

    def getFrame(self):
        try:
            return self.drone.get_frame_read()
        except:
            return None

            
