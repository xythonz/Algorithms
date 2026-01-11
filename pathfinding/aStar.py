# A* Algorithm
from queue import PriorityQueue
import math

def pathfind(graph, start, goal, positions):
    def euclidean_distance(a, b):
        """Calculate Euclidean distance between two nodes using their positions"""
        x1, y1 = positions[a]
        x2, y2 = positions[b]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = euclidean_distance(start, goal)

    while not open_set.empty():
        current = open_set.get()[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path = path[::-1]
            return path, g_score[goal]

        for neighbor, weight in graph[current].items():
            tentative_g_score = g_score[current] + weight

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + euclidean_distance(neighbor, goal)
                if not any(neighbor == item[1] for item in open_set.queue):
                    open_set.put((f_score[neighbor], neighbor))

    return [], None