from scipy.optimize import fsolve
import math 
from sympy import Eq, solve, sqrt, symbols


def sympy_solver():
    x, y = symbols('x y')
    eq1 = Eq(sqrt(x**2 + y**2), t1)
    eq2 = Eq(sqrt((10-y)**2 + (10*x/(20-y)-x)**2) + sqrt(10**2 + (10*x/(20-y))**2), t2)
    eq3 = Eq(sqrt((15-x)**2 + (15*y/(30-x)-y)**2) + sqrt(15**2 + (15*y/(30-x))**2), t3)
    solved = solve((eq1, eq2), (x, y))
    return solved




def get_equations(variables):
    (x, y) = variables
    eq1 = sqrt(x**2 + y**2) - t1
    t2_t1_ratio = t2/t1
    eq2 = math.sqrt((10-y)**2 + (10*x/(20-y)-x)**2) + math.sqrt(10**2 + (10*x/(20-y))**2) - t2
    eq3 = math.sqrt((15-x)**2 + (15*y/(30-x)-y)**2) + math.sqrt(15**2 + (15*y/(30-x))**2) - t3
    return [eq1, eq2]



def get_times(x, y):
    est_t1 = sqrt(x**2 + y**2)
    est_t2 = sqrt((10-y)**2 + (10*x/(20-y)-x)**2) + sqrt(10**2 + (10*x/(20-y))**2)
    est_t3 = sqrt((15-x)**2 + (15*y/(30-x)-y)**2) + sqrt(15**2 + (15*y/(30-x))**2)
    return (est_t1, est_t2, est_t3)




sympy_solver




# get_equations((8,8))
# sympy_solver()
t1 = 16.74922
t2 = 25.8702747 
t3 = 36.32250459

import ipdb; ipdb.set_trace()
solutions = fsolve(get_equations, (5, 7.5))
if len(solutions) == 2:
    x, y = solutions
    print(f"({x}, {y})")

t1 = 11.3137084989848
t2 = 12.0148075307098+2.4075042421643
t3 = 15.9609544221552+7.448445399284
solutions = fsolve(get_equations, (5, 7.5))
if len(solutions) == 2:
    x, y = solutions
    print(f"({x}, {y})")



