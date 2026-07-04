from enum import Enum

class LiftStatus(Enum):
    Running = "Running",
    Stationary = "Stationary"

class Direction(Enum):
    Up = "Up",
    Down = "Down"