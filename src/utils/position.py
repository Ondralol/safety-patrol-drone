from dataclasses import dataclass

@dataclass
class Position:
    x: float
    y: float
    z: float
    angle: float  # yaw in degrees