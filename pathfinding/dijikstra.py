# Dijkstra's Algorithm
import heapq

def pathfind(graph, start, goal):
    queue = []
    heapq.heappush(queue, (0, start))
    distances = {node: float('inf') for node in graph}
    predecessors = {node: None for node in graph}
    distances[start] = 0

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        if current_node == goal:
            break

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    if distances[goal] == float('inf'):
        return [], None

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    path.reverse()
    return path, distances[goal]