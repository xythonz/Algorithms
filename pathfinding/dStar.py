# D* Lite Algorithm (simplified for static graph pathfinding)
# For static graphs, D* Lite reduces to backward A*
import heapq
import math

def pathfind(graph, start, goal, positions):
    def euclidean_distance(a, b):
        """Calculate Euclidean distance between two nodes using their positions"""
        x1, y1 = positions[a]
        x2, y2 = positions[b]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # D* Lite works backward from goal to start
    # Priority queue: (f_score, g_score, node)
    # f_score = g_score + heuristic (where heuristic is distance to start for backward search)
    pq = [(euclidean_distance(goal, start), 0, goal)]
    g_score = {node: float('inf') for node in graph}
    g_score[goal] = 0
    came_from = {}
    visited = set()

    while pq:
        _, current_dist, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)

        if current == start:
            break

        # Look at all neighbors (going backward in the graph)
        # For undirected graphs, this means looking at nodes that connect to current
        for node in graph:
            if current in graph[node]:  # If there's an edge from node to current
                weight = graph[node][current]
                new_g_score = current_dist + weight

                if new_g_score < g_score[node]:
                    g_score[node] = new_g_score
                    came_from[node] = current
                    f_score = new_g_score + euclidean_distance(node, start)
                    heapq.heappush(pq, (f_score, new_g_score, node))

    # Check if path exists
    if g_score[start] == float('inf'):
        return [], None

    # Reconstruct path from start to goal
    path = []
    current = start
    while current != goal:
        path.append(current)
        if current not in came_from:
            return [], None
        current = came_from[current]
    path.append(goal)

    return path, g_score[start]