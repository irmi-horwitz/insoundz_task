import matplotlib.pyplot as plt
import numpy as np
import math

plt.xlim(-30,30)
plt.ylim(-30,30)

def calculate_direct_line(y, t):

    if t**2 > y**2:
        return math.sqrt(t**2 - y**2)
    return 0


def get_rbounce_len_and_point(mag, rad):
    bx = 15*np.tan(rad)
    length = np.sqrt(15**2 + bx**2)
    return (mag-length, (15, bx))

def get_tbounce_len_and_point(mag, rad):
    by = 10*np.tan(rad)
    length = np.sqrt(10**2 + by**2)
    return (mag-length, (by, 10))

def deg_to_rad(deg):
    return deg*(math.pi/180)

def get_xy(mag, deg):
    return (mag*np.cos(deg), mag*np.sin(deg))

def plot_points(points, color='red'):
    x_list = []
    y_list= []
    for x, y in points:
        # if x <= 15 and y <= 10:
        x_list.append(x)
        y_list.append(y)

    plt.scatter(x_list, y_list)



t1 = 16.74922
t2 = 25.8702747
t3 = 36.32250459

coordinates = []
for i in range(360):
    rad = deg_to_rad(i)

    print(get_xy(t1, rad))
    t1_pair = get_xy(t1, rad)
    t2_mag, t2_start = get_tbounce_len_and_point(t2, rad)
    t2_pair = get_xy(t2_mag, rad)
    t2_pair = (t2_pair[0] + t2_start[0], t2_pair[1] + t2_start[1])

    t3_mag, t3_start = get_tbounce_len_and_point(t3, rad)
    t3_pair = get_xy(t3_mag, rad)
    t3_pair = (t3_pair[0] + t3_start[0], t3_pair[1] + t3_start[1])
    coordinates.append(t1_pair)
    coordinates.append(t2_pair)
    coordinates.append(t3_pair)

plot_points(coordinates)

# plt.scatter([6.6666666666666, 8, 15], [10, 8, 5.454545454545], color='red')
plt.show()  