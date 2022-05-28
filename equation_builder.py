from sympy import sqrt

class EquationBuilder:
    """
    This class builds the equations for calculating clap's position based on recording times or vice versa.
    More detail on the maths itself can be found in the README file.
    """
    @staticmethod
    def get_direct_eq(clap_location, room):
        """
        Get the equation for a straight line between mic and clap.
        Args:
            clap_location: Tuple of (x, y) ints
            room: Room object.
        Returns: 
            Time or Equation for calculating sound path's time from clap to mic. equation is used to calculate position of clap.
        """
        x, y = clap_location
        mX, mY = room.mic.coordinates
        return sqrt((x-mX)**2 + (y-mY)**2)

    def build_equations(self, clap_location, room, wall_position):
        """
        build the equations for wall reflections.
        Args:
            clap_location: Tuple of (x, y) ints
            room: Room object.
            wall_position; 'top' or 'right', depending on desired wall's equation.
        Returns: 
            Time or Equation for calculating sound path's time from clap to mic. equation is used to calculate position of clap.
        """
        x, y = clap_location
        mX, mY = room.mic.coordinates

        if wall_position == 'top':
            (aX, aY) = self.get_top_wall_intersection(clap_location, room)
        elif wall_position == 'right':
            (aX, aY) = self.get_right_wall_intersection(clap_location, room)
            
        else:
            raise Exception('wall_position must be either top or right')

        return sqrt((x-aX)**2 + (y-aY)**2) + sqrt((aX-mX)**2 + (aY-mY)**2)

    @staticmethod
    def get_top_wall_intersection(clap_location, room):
        """
        Get the position of sound reflection off top wall.
        Args:
            clap_location: Tuple of (x, y) ints
            room: Room object.
        Returns: 
            Coordinates or equation of coordinated for point of reflection on top wall.
        """
        x, y = clap_location
        mX, mY = room.mic.coordinates
        h = room.top_wall.wall_limit

        g = (2*h-y-mY)/(x-mX)
        return (h/g+mX-mX/g, h)

    @staticmethod
    def get_right_wall_intersection(clap_location, room):
        """
        Get the position of sound reflection off right wall.
        Args:
            clap_location: Tuple of (x, y) ints
            room: Room object
        Returns: 
            Coordinates or equation of coordinated for point of reflection on right wall.
        """
        x, y = clap_location
        mX, mY = room.mic.coordinates
        aX = w = room.right_wall.wall_limit

        g = (y-mY)/(2*w-x-mX)
        return (w, g*w+mX-g*mX)

