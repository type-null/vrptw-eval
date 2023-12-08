import math


def calculate_distance(x, y):
    total_distance = 0

    # Iterate through pairs of consecutive coordinates
    for i in range(1, len(x)):
        x1, y1 = x[i - 1], y[i - 1]
        x2, y2 = x[i], y[i]

        # Calculate the distance between consecutive points
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        # Accumulate the distance
        total_distance += distance

    return total_distance


x = [-1.41, -24.94]

y = [70.60, 91.32]


print(calculate_distance(x, y))
