from typing import List, Tuple
from sympy import sqrt



class Wall:
    """
    class representing a wall
    """
    time = None
    def __init__(self, wall_position: str, wall_limit: int = 0, reflection_time: int = None):
        self.reflection_time = reflection_time
        self.wall_position = wall_position
        self.wall_limit = wall_limit

class Mic:
    """
    class representing a microphone
    """
    def __init__(self, x: int, y: int, times: List[int]=None):
        self.coordinates = (x, y)
        self.times = times

