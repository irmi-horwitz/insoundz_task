from typing import List, Tuple

from equation_solver import EquationSolver
from room import Room, RoomConfig
from wall import Wall, Mic


reflection_times = [16.74922, 25.8702747 , 36.32250459]
reflection_times = [11.3137084989848, 12.0148075307098+2.4075042421643, 15.9609544221552+7.448445399284]


def clap_event(room, times: List=None, clap_location: Tuple=None):
    """
    This function simulates a clap in the room. 
    Following a clap, one of two things can happen:
        -The listener knows where the clap is, and will start recording, returning the times it took for the clap to reach home.
        -The listener will use the times it took for the clap to reach him to calculate the position of the clap.

    If times argument is provided, the EquationSolver will try to calculate the clap position.
    If not, and clap_location is provided, a list of times will be returned.

    Args:m
        room: The room in which the clap event has occured.
        times: List of times it took for the clap to reach the Mic.
        clap_location: (x, y) tuple of clap location for time measurements,
    """
    if times is None and clap_location is None:
        raise Exception("either clap location or clap times must have a value")

    if times:
        solver = EquationSolver(room)
        room.mic.times = times
        return solver.solve_for_location()
    
    if clap_location:
        return room.infer_time(clap_location)
    return None

def create_room():
    """
    Creates a dummy room with mic at (0,0), wall at x=15, and wall at y=10.
    """
    mic = Mic(0,0, times=reflection_times)
    right_wall = Wall(wall_position='right', wall_limit=15)
    top_wall = Wall(wall_position='top', wall_limit=15)

    return Room(mic=mic, right_wall=right_wall, top_wall=top_wall)



def run_decimal_positions():
    """
    Just for testing and demonstration purposes.
    iterates over x and y integers and tests both time inference and position inference.
    """
    times = {}
    room = create_room()
    for x in range(1,15):
        for y in range(1,10):
            if x == room.mic.coordinates[0] or y == room.mic.coordinates[1]:
                continue
            times[x,y] = clap_event(room, clap_location=(x, y))

    for pos, rec_time in times.items():
        res = clap_event(room, times=rec_time)
        print(f"pos: {pos}\ntime: {rec_time}\nresult:{res}")


run_decimal_positions()