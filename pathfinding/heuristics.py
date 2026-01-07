def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def euclidean_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def chebyshev_distance(point1, point2):
    return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))

def diagonal_distance(point1, point2):
    return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))

def octile_distance(point1, point2):
    dx = abs(point1[0] - point2[0])
    dy = abs(point1[1] - point2[1])
    return (dx + dy) + (2**0.5 - 2) * min(dx, dy)