import numpy as np
import math


MAX_CALIBRATION = 200
PIEZO_SENSOR_DISTANCE = 10
R = (abs(PIEZO_SENSOR_DISTANCE - MAX_CALIBRATION) * math.sqrt(3) / 3)
r = (abs(PIEZO_SENSOR_DISTANCE - MAX_CALIBRATION) * math.sqrt(3) / 6)
a = (abs(PIEZO_SENSOR_DISTANCE - MAX_CALIBRATION))
p1 = np.array([-a / 2, -r])
p2 = np.array([0, R])
p3 = np.array([a / 2, -r])
delta = 0.4
min_impulse = 10


def calculate(q, q2):
    data = q.get()
    ip = []
    values = []

    for i, j in data:
        ip.append(i)
        values.append(j)

    print(f"======\nIn function 'calculate':")
    for i in range(0, len(values)):
        values[i] = norm(values[i])

    for i in range(0, len(values)):
        if not have_impulse(values[i], min_impulse):
            print("NoInput 1")
            q2.put("")
            return

    if not check_peaks(values[0], values[1], values[2], delta):
        print("NoInput 2")
        q2.put("")
        return

    maxes = get_maxes(values[0], values[1], values[2])
    max1 = (maxes[0][0] + maxes[0][1]) / 2
    max2 = (maxes[1][0] + maxes[1][1]) / 2
    max3 = (maxes[2][0] + maxes[2][1]) / 2

    d1 = abs(max1 - MAX_CALIBRATION)
    d2 = abs(max2 - MAX_CALIBRATION)
    d3 = abs(max3 - MAX_CALIBRATION)

    print(f"{ip[0]}: {d1=}\n"
          f"{ip[1]}: {d2=}\n"
          f"{ip[2]}: {d3=}")

    x, y = trilateration(p1, p2, p3, d1, d2, d3)

    print(f"The coordinates of the point are: {x=}, {y=}")
    direction = calc_hit_pos(x, y)
    print(direction)
    q2.put(direction)
    print("======")


def norm(data):
    median = np.median(data)
    for i in range(0, len(data)):
        data[i] -= median
    return data


def have_impulse(data: list, min_impulse: float) -> bool:
    return max(data) > min_impulse


def check_peaks(data1: list, data2: list, data3: list, delta: float = 0.4) -> bool:
    maxes = get_maxes(data1, data2, data3)
    max_prop_1 = maxes[0][1] / maxes[0][0]
    max_prop_2 = maxes[1][1] / maxes[1][0]
    max_prop_3 = maxes[2][1] / maxes[2][0]

    print(f"{max_prop_1:.2f}, {max_prop_2:.2f}, {max_prop_3:.2f}")

    if math.isclose(max_prop_1, max_prop_2, rel_tol=delta) and math.isclose(max_prop_2, max_prop_3, rel_tol=delta):

        return True
    return False


def get_maxes(data1: list, data2: list, data3: list) -> list:
    max1_1 = max(data1)
    data1.remove(max1_1)
    max1_2 = max(data1)

    max2_1 = max(data2)
    data2.remove(max2_1)
    max2_2 = max(data2)

    max3_1 = max(data3)
    data3.remove(max3_1)
    max3_2 = max(data3)

    return [[max1_1, max1_2], [max2_1, max2_2], [max3_1, max3_2]]


def trilateration(p1, p2, p3, d1, d2, d3):
    """
    Trilateration algorithm to find (x, y) coordinates of a point in 2D space given the distances
    from the point to three other points with known coordinates.

    Parameters:
    p1, p2, p3: arrays with (x, y) coordinates of three points
    p1, p2, p3: distances from the unknown point to each of the three points

    Returns:
    (x, y): the coordinates of the unknown point
    """
    # Calculate the vectors from the first point to the other two points
    A = 2 * np.array([p2 - p1, p3 - p1])
    b = np.array([d1**2 - d2**2 + np.dot(p2, p2) - np.dot(p1, p1),
                  d1**2 - d3**2 + np.dot(p3, p3) - np.dot(p1, p1)])
    p = np.linalg.solve(A, b)
    return p[0], p[1]


def is_point_in_circle(x, y, center_x, center_y, radius):
    distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
    return distance <= radius


def calc_hit_pos(x, y):
    if(is_point_in_circle(x, y, 0, 0, R / 5)):
        return "ZoomIn"
    else:
        return get_quoter(x, y)


def get_quoter(x, y):
    # Define the angle of rotation (in degrees)
    angle = 45

# Convert the angle to radians
    theta = np.deg2rad(angle)

# Define the rotation matrix
    rot = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta), np.cos(theta)]])

# Calculate the point's coordinates in the unrotated coordinate system
    x_unrotated, y_unrotated = np.dot(rot.T, np.array([x, y]))

# Determine the quadrant of the point based on its unrotated coordinates
    if x_unrotated > 0 and y_unrotated > 0:
        return "MoveUp"
    elif x_unrotated < 0 and y_unrotated > 0:
        return "MoveLeft"
    elif x_unrotated < 0 and y_unrotated < 0:
        return "MoveDown"
    else:
        return "MoveRight"