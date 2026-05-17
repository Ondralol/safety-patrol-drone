import math
from djitellopy import tello, Tello
from enum import Enum, IntEnum, StrEnum
import threading
import time
from utils.position import Position

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

# Drone number: 07
RC_SPEED_TO_CMS = 0.85 # We need to calibrate this

class Drone:
    def __init__(self):
        self.drone = tello.Tello()

        # Relative position
        self.position = Position(0, 0, 0, 0)

        self._cancel_event = threading.Event()

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
        self.position.z += 70
    
    def keepAlive(self):
        try:                                                                                                                                          
          self.drone.send_command_without_return("command")
        except:                                                                                                                                       
          pass  

    def land(self):
        self._cancel_event.set()
        if hasattr(self, '_worker') and self._worker.is_alive():
            self._worker.join(timeout=7.0)
        self.drone.land()
        self.position.z = 0
        self._cancel_event.clear()


    def startStream(self):
        self._run(self.drone.streamon)


    def stopStream(self):
        self._run(self.drone.streamoff)


    def emergency(self):
        # Run instantly, not in a thread
        self.drone.emergency()
        self.position.z = 0


    def enableMissionPads(self):
        self._run(self.drone.enable_mission_pads)

    def moveSmall(self, dir: DIRECTION, x_cm: int, in_thread: bool = True):
        """Uses rc control to move precisely (cm accuracy)."""

        speed = SPEED.MEDIUM
        estimated_cms = speed * RC_SPEED_TO_CMS
        duration = x_cm / estimated_cms

        lr, fb, ud = 0, 0, 0
        if   dir is DIRECTION.FORWARD: fb =  speed
        elif dir is DIRECTION.BACK:    fb = -speed
        elif dir is DIRECTION.LEFT:    lr = -speed
        elif dir is DIRECTION.RIGHT:   lr =  speed
        elif dir is DIRECTION.UP:      ud =  speed
        elif dir is DIRECTION.DOWN:    ud = -speed

        RC_INTERVAL = 0.05  # 20 Hz keep alive
        # The pc needs to send the rc signals constantly

        def _go():
            elapsed = 0.0
            while elapsed < duration:
                self.drone.send_rc_control(lr, fb, ud, 0)
                time.sleep(RC_INTERVAL)
                elapsed += RC_INTERVAL
            self.drone.send_rc_control(0, 0, 0, 0)

        if in_thread:
            self._run(_go)
        else:
            _go()

        # Dead reckoning position update
        a = math.radians(self.position.angle)
        if dir is DIRECTION.FORWARD:
            self.position.x += x_cm * math.cos(a)
            self.position.y += x_cm * math.sin(a)
        elif dir is DIRECTION.BACK:
            self.position.x -= x_cm * math.cos(a)
            self.position.y -= x_cm * math.sin(a)
        elif dir is DIRECTION.LEFT:
            self.position.x += x_cm * math.sin(a)
            self.position.y -= x_cm * math.cos(a)
        elif dir is DIRECTION.RIGHT:
            self.position.x -= x_cm * math.sin(a)
            self.position.y += x_cm * math.cos(a)
        elif dir is DIRECTION.UP:
            self.position.z += x_cm
        elif dir is DIRECTION.DOWN:
            self.position.z -= x_cm

    def move(self, dir: DIRECTION, x: int, in_thread = True):
        """Fly x cm in direction dir."""
        if in_thread:
            self._run(lambda: self.drone.move(dir, x))
        else:
            self.drone.move(dir, x)

        a = math.radians(self.position.angle)
        if dir is DIRECTION.FORWARD:
            self.position.x += x * math.cos(a)
            self.position.y += x * math.sin(a)
        elif dir is DIRECTION.BACK:
            self.position.x -= x * math.cos(a)
            self.position.y -= x * math.sin(a)
        elif dir is DIRECTION.LEFT:
            self.position.x += x * math.sin(a)
            self.position.y -= x * math.cos(a)
        elif dir is DIRECTION.RIGHT:
            self.position.x -= x * math.sin(a)
            self.position.y += x * math.cos(a)
        elif dir is DIRECTION.UP:
            self.position.z += x
        elif dir is DIRECTION.DOWN:
            self.position.z -= x


    def moveToXYZRelativeToCurrentPosition(self, x: int, y: int, z: int, speed: SPEED,  in_thread = True):
        if in_thread:
            self._run(lambda: self.drone.go_xyz_speed(x, y, z, speed))
        else:
            self.drone.go_xyz_speed(x, y, z, speed)


        # Correctly update the position
        a = math.radians(self.position.angle)
        self.position.x += x * math.cos(a) - y * math.sin(a)
        self.position.y += x * math.sin(a) + y * math.cos(a)
        self.position.z += z


    def moveToXYZRelativeToPad(self, x: int, y: int, z: int, speed: SPEED, pad: int, in_thread = True):
        if in_thread:
            self._run(lambda: self.drone.go_xyz_speed_mid(x, y, z, speed, pad))
        else:
            self.drone.go_xyz_speed_mid(x, y, z, speed, pad)

        # Update postion
        self.position.x = x
        self.position.y = y
        self.position.z = z
        


    def rotate(self, dir: ROTATION_DIRECTION, angle_deg: int, in_thread = True):
        if in_thread:
            if dir is ROTATION_DIRECTION.CLOCKWISE:
                self._run(lambda: self.drone.rotate_clockwise(angle_deg))
            elif dir is ROTATION_DIRECTION.COUNTERCLOCKWISE:
                self._run(lambda: self.drone.rotate_counter_clockwise(angle_deg))
        else:
            if dir is ROTATION_DIRECTION.CLOCKWISE:
                self.drone.rotate_clockwise(angle_deg)
            elif dir is ROTATION_DIRECTION.COUNTERCLOCKWISE:
                self.drone.rotate_counter_clockwise(angle_deg)

        if dir is ROTATION_DIRECTION.CLOCKWISE:
            self.position.angle += angle_deg
        elif dir is ROTATION_DIRECTION.COUNTERCLOCKWISE:
            self.position.angle -= angle_deg


    def _expand_move(self, dir: DIRECTION, total_cm: int, speed: SPEED, step_cm: int = 10, pause: float = 0.75):
        # Creates small steps
        steps = []
        remaining = total_cm
        while remaining > 0:
            chunk = min(step_cm, remaining)
            steps.append((lambda d=dir, c=chunk: self.moveSmall(d, c, in_thread=False), pause))
            remaining -= chunk
        return steps

    def _expand_rotate(self, dir: ROTATION_DIRECTION, total_deg: int, step_deg: int = 15, pause: float = 1.75):
        # Creates small steps

        # Fix the offset
        ROTATION_OFFSET = 5 # TODO TRY 6, might be good
        if dir is ROTATION_DIRECTION.CLOCKWISE:
            self.position.angle += ROTATION_OFFSET
        else:
            self.position.angle -= ROTATION_OFFSET
        

        steps = []
        remaining = total_deg
        while remaining > 0:
            chunk = min(step_deg, remaining)
            steps.append((lambda d=dir, c=chunk: self.rotate(d, c, in_thread=False), pause))
            remaining -= chunk
        return steps

    def _buildInspectSequence(self, speed: SPEED):
        seq = []
        
        OFFSET = 10

        # Moving to left side
        seq += self._expand_rotate(ROTATION_DIRECTION.COUNTERCLOCKWISE, 45)
        seq += self._expand_move(DIRECTION.FORWARD, 25 - OFFSET, speed)
        seq += self._expand_rotate(ROTATION_DIRECTION.CLOCKWISE, 90)
        seq += self._expand_move(DIRECTION.LEFT, 50 - OFFSET, speed)
        # Go back to the starting point
        seq += self._expand_move(DIRECTION.RIGHT, 50 - OFFSET, speed)
        seq += self._expand_rotate(ROTATION_DIRECTION.COUNTERCLOCKWISE, 90)
        seq += self._expand_move(DIRECTION.BACK, 20 - OFFSET, speed)
        seq += self._expand_rotate(ROTATION_DIRECTION.CLOCKWISE, 45)
        # Moving to right side
        seq += self._expand_rotate(ROTATION_DIRECTION.CLOCKWISE, 45)
        seq += self._expand_move(DIRECTION.FORWARD, 25 - OFFSET, speed)
        seq += self._expand_rotate(ROTATION_DIRECTION.COUNTERCLOCKWISE, 90)
        seq += self._expand_move(DIRECTION.RIGHT, 50 - OFFSET, speed)
        # Go back to the starting point
        seq += self._expand_move(DIRECTION.LEFT, 50 - OFFSET, speed)
        seq += self._expand_rotate(ROTATION_DIRECTION.CLOCKWISE, 90)
        seq += self._expand_move(DIRECTION.BACK, 20 - OFFSET, speed)
        seq += self._expand_rotate(ROTATION_DIRECTION.COUNTERCLOCKWISE, 45)
        return seq
    


    def inspectObject(self, on_done = None, speed: SPEED = SPEED.SLOW):
        """Inspect an object by sweeping left then right."""
        def _run_sequence():
            self._cancel_event.clear()
            for step, timeout in self._buildInspectSequence(speed):
                if self._cancel_event.is_set():
                    break
                step()
                self._cancel_event.wait(timeout)
            if on_done is not None and not self._cancel_event.is_set():
                on_done()

        self._run(_run_sequence)


    def _build_sequence(self):
        seq = []
        # Moving to top left corner
        seq += self._expand_rotate(ROTATION_DIRECTION.COUNTERCLOCKWISE, 45)
        seq += self._expand_move(DIRECTION.FORWARD, 100, SPEED.MEDIUM)
        seq += self._expand_rotate(ROTATION_DIRECTION.CLOCKWISE, 135)
        # Moving in a square around grid
        seq += self._expand_move(DIRECTION.FORWARD, 150, SPEED.MEDIUM)
        seq += self._expand_rotate(ROTATION_DIRECTION.CLOCKWISE, 90)
        seq += self._expand_move(DIRECTION.FORWARD, 150, SPEED.MEDIUM)
        seq += self._expand_rotate(ROTATION_DIRECTION.CLOCKWISE, 90)
        seq += self._expand_move(DIRECTION.FORWARD, 150, SPEED.MEDIUM)
        seq += self._expand_rotate(ROTATION_DIRECTION.CLOCKWISE, 90)
        seq += self._expand_move(DIRECTION.FORWARD, 150, SPEED.MEDIUM)
        seq += self._expand_rotate(ROTATION_DIRECTION.CLOCKWISE, 135)
        # Moving in a diagonal around grid
        seq += self._expand_move(DIRECTION.FORWARD, 180, SPEED.MEDIUM)
        seq += self._expand_rotate(ROTATION_DIRECTION.CLOCKWISE, 135)
        seq += self._expand_move(DIRECTION.FORWARD, 150, SPEED.MEDIUM)
        seq += self._expand_rotate(ROTATION_DIRECTION.CLOCKWISE, 135)
        seq += self._expand_move(DIRECTION.FORWARD, 180, SPEED.MEDIUM)
        seq += self._expand_rotate(ROTATION_DIRECTION.CLOCKWISE, 180)
        seq += self._expand_move(DIRECTION.FORWARD, 90, SPEED.MEDIUM)
        seq += self._expand_rotate(ROTATION_DIRECTION.CLOCKWISE, 135)
        return seq
    

    def startSequence(self):
        """Fly predefined perimeter path."""
        def _run_sequence():
            self._cancel_event.clear()
            for step, timeout in self._build_sequence():
                if self._cancel_event.is_set():
                    break
                step()
                self._cancel_event.wait(timeout)
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

            
