from sympy import Eq, nsolve, symbols, CoercionFailed
from typing import Tuple, List
from itertools import combinations
import math

from room import Room


class EquationSolver:
    """
    The equation solver. Takes a room and reflection times, and tries to solve for clap location.
    After solving the location, it checks that the results make sense and are within the borders of the room,
    Example:
    >>> times = [10, 11, 12]
    >>> room = Room(mic=mic, right-wall=right_wall, left_wall=left_wall)
    >>> solver = EquationSolver(room)
    >>> results = solver.solve_for_location(times=times)

    Args:
        room: Room object to use for calculations.
    """

    def __init__(self, room: Room):
        self.room = room
    
    def solve_for_location(self) -> List[Tuple]:
        """
        Generates estimates to attribute time to specific wall. 
        Iterates over those estimations, and for each estimation, tries to solve the equation. 
        If it fails, it goes to the next extimation. If succeeds, adds it to results to be checked later.
        Args:
            times: List of recording times.
        return:
            list of Tuples possible clap locations.
        """
        
        def get_wall_equations(variables, reordered_times):
            """
            Gets all equations, turns them into sympy.Eq and adds them to a list.
            Args:
                list of times for reflections.
            Returns:
                List of equations.
            """
            r_wall_eq = self.room.build_equations(variables, 'right')
            top_wall_eq = self.room.build_equations(variables, 'top')
            equations = [Eq(r_wall_eq, reordered_times[0]),
                         Eq(top_wall_eq, reordered_times[1])]
            return equations


        times = self.room.mic.times
        wall_order_estimates = self.room.reflection_order_estimator(times)
        results = []
        x, y = symbols('x y')
        for reflection_order in wall_order_estimates:
            equations = get_wall_equations((x, y), reflection_order)
            try:
                results.append(nsolve(equations, (x, y), (7,7), verify=False, dict=True))
            except (NotImplementedError, CoercionFailed)  as e:
                pass


        return self._check_results(results, (x, y))


    def _check_results(self, results: List[Tuple], variables: Tuple) -> List[Tuple]:
        """
        Iterate over results and check if they are valid.
        Args:
            results: list of (x, y) pairs
            variables: Tuple of sympy.symbols object.
        Returns:variables
            List of goodn(x, y) pairs
        
        """
        good_results = []
        for result in results:
            if isinstance(result, list):
                result_dict = result[0]
            else:
                result_dict = result
            if self._check_single_result(result_dict, variables):
                good_results.append(result)

        return good_results

    def _check_single_result(self, result: Tuple, variables: Tuple) -> bool:
        """
        Checks if (x, y) pair is possible for clap.
        A pair os possiblefor clap if:
            -Both numbers are real
            -Neither number is out of it's exis bounds.
        Args:
            result: Single (x, y) pair representing possible clap location.
        Returns;
            True if position is possible, False otherwise.
        """
        x, y = variables
        x_result = result[x]
        y_result = result[y]

        if not x_result.is_real or not y_result.is_real:
            return False
        if x_result < self.room.x_limit[0] or x_result > self.room.x_limit[1]:
            return False    
        if y_result < self.room.y_limit[0] or y_result > self.room.y_limit[1]:
            return False


        direct = self.room.get_direct_line_equation((x_result, y_result))
        
        return math.isclose(direct, self.room.direct_line_time, rel_tol=0.001)
