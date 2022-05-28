from itertools import permutations
from dataclasses import dataclass
from typing import List, Tuple
from ctypes import Union
from equation_builder import EquationBuilder


from wall import Mic, Wall

@dataclass
class RoomConfig:
    """
    This dataclass represents a room's configuration. 
    It can be loaded from and saved to file , or it can be manually set, then passed to Room init.
    right_wall_limit: right wall's position. In the provided example, this equals 15(x=15)
    top_wall_limit: top wall's position. In the provided example, this equals 10(y=10)
    mic: Tuple representing mic's (x, y) position
    clap_location: Tuple representing clap's (x, y) position.
    """
    right_wall_limit: int
    top_wall_limit: int
    mic: Mic
    clap_location: Tuple

    def load_from_file(file_path: str):
        """
        Loads file config from file.
        Args:
            file_path: config file path
        """
        pass
    
    def save_to_file(file_path: str):
        """
        Saves config to file.
        Args:
            file_path: destination config file path
        """
        pass

class Room:
    """
    Class that represents a room.
    A room contains:
        -two walls(one top_wall and one right_wall)
        -A Microphone
        -A clap
    The clap position has to be set in order to infer recording times.

    Room has the options to build a reflection's equation, to estimate the order in which the reflections arrived,
    and to calculate the recording times based on clap location and mic location.
    Example:
    >>> right_wall = Wall(wall_position='right', wall_limit=15)
    >>> top_wall = Wall(wall_position='left',wall_limit=10)
    >>> mic = Mic(0,0)
    >>> room = Room(mic=mic, right_wall=right_wall, top_wall=top_wall)
    >>> room.build_equations()
    >>> times = room.infer_time(clap_location=(8, 8))

    Args:
        top_wall: Room's top wall.
        right_wall: Room's right wall.
        mic: Microphone's location.
        clap_location: Clap's location in the room. Optional, required if infer_time is to be used.
        room_config: Instead of providing config manually, one can just pass a RoomConfig object.
    """
    room_conf = RoomConfig
    def __init__(self, top_wall: Wall,
                       right_wall: Wall,
                       mic: Mic,
                       lower_x_limit: int = 0,
                       lower_y_limit: int = 0,
                       room_config: RoomConfig = None):

        if room_config:
            self.room_conf = room_config
        else:
            self.mic = mic
            self.x_limit = (lower_x_limit, right_wall.wall_limit)
            self.y_limit = (lower_y_limit, top_wall.wall_limit)
            self.top_wall = top_wall
            self.right_wall = right_wall

    def build_equations(self, clap_location, wall_position):
        """
        Build the equations to solve clap's location in the room based on times, or to solve times based on clap's location.
        Uses EquationBuilder.
        Args:
            variables: Tuple of (x, y) sympy.symbols, or real (x, y) coordinates if infer_time is used.
            wall_position: str: 'right' or 'top' indicating which equation to return
        Returns:
            int if clap_location is real numbers, sympy.Eq if clap_location if sympy.sympols.
        """
        return EquationBuilder().build_equations(clap_location, self, wall_position)

    def reflection_order_estimator(self, times: List) -> List[Tuple]:
        """
        meant to estimate the order in which the walls reflected the sound.
        Since the microphone is not directinal, we have no simple way of knowing which wall reflected which sound peak.
        The only peak we know to attribute for sure is the shortest one, as it has to belong to the straight line from clap to mic.
        For now, it has not logic, but with abit of work it is possible to make this a smart estimator, 
        taking into account relations between the wall locations, mic location, and many more attributes.
        Args:
            times: a list of [t1, t2, t3] representing the peaks detected in the recording since t0/
        returns:
            List of all permutations of times Except for direct_line_time, hwich is always the shortest
        """
        sorted_times = sorted(times)
        self.direct_line_time = sorted_times[0]
        wall_reflection_times = sorted_times[1:]
        return list(permutations(wall_reflection_times))

    def get_direct_line_equation(self, clap_location: Tuple):
        """
        Returns the equation for direct line between mic and clap.
        Args: 
            variables: Tuple of (x, y) sympy.symbols, or real (x, y) coordinates if infer_time is used.
        Returns:
            int if clap_location is real numbers, sympy.Eq if clap_location if sympy.sympols.
        """
        return EquationBuilder().get_direct_eq(clap_location, self)

    def infer_time(self, clap_location: Tuple) -> int:
        """
        Calculate how long it takes for the sound to arrive to mic from each direction:
        straight line, reflection off top wall, and reflection off right wall.
        Args:
            clap_location: Tuple of (x, y) ints
        Returns: 
            list of times it took each path to arrive to mic.
        """
        direct_line = EquationBuilder().get_direct_eq(clap_location, self)
        r_time = EquationBuilder().build_equations(clap_location, self, self.right_wall.wall_position)
        t_time = EquationBuilder().build_equations(clap_location, self, self.top_wall.wall_position)
        times = [direct_line, r_time, t_time]

        return sorted(times)

    def _load_from_config(self, room_config):
        pass