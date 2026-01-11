from collections import deque

def pathfind(graph, start, goal):
    if start not in graph or goal not in graph:
        return [], float('inf')
    
    queue = deque([start])
    visited = {start: None}
    distances = {start: 0}
    
    while queue:
        current = queue.popleft()
        
        if current == goal:
            break
        
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited[neighbor] = current
                distances[neighbor] = distances[current] + 1  # Each edge has weight 1
                queue.append(neighbor)
    
    if goal not in visited:
        return [], float('inf')
    
    # Reconstruct path
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = visited[current]
    path.reverse()
    
    return path, distances[goal]