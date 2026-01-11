# Bellman-Ford Algorithm
def pathfind(graph, start, goal):
    distances = {node: float('inf') for node in graph}
    predecessors = {node: None for node in graph}
    distances[start] = 0

    for _ in range(len(graph) - 1):
        updated = False
        for u in graph:
            for v, weight in graph[u].items():
                if distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    predecessors[v] = u
                    updated = True
        if not updated:
            break

    for u in graph:
        for v, weight in graph[u].items():
            if distances[u] + weight < distances[v]:
                raise ValueError("Graph contains a negative-weight cycle")

    if distances[goal] == float('inf'):
        return [], None

    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = predecessors[current]
    
    path.reverse()
    return path, distances[goal]