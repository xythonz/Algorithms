def manhattan_distance(point1, point2):
    """Calculates the Manhattan distance between two points in a grid."""
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def euclidean_distance(point1, point2):
    """Calculates the Euclidean distance between two points in a grid."""
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

def chebyshev_distance(point1, point2):
    """Calculates the Chebyshev distance between two points in a grid."""
    return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))

def zero_heuristic(point1, point2):
    """A heuristic that always returns zero, effectively making A* behave like Dijkstra's algorithm."""
    return 0

def diagonal_distance(point1, point2):
    """Calculates the Diagonal distance between two points in a grid."""
    return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))

def octile_distance(point1, point2):
    """Calculates the Octile distance between two points in a grid."""
    dx = abs(point1[0] - point2[0])
    dy = abs(point1[1] - point2[1])
    return (dx + dy) + (2**0.5 - 2) * min(dx, dy)