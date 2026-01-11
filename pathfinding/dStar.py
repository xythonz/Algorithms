# D* Algorithm
import heapq

def pathfind(grid, start, goal):
    def heuristic(a, b):
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return dx + dy
    
    def get_neighbors(node):
        x, y = node
        neighbors = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
                cost = 1.414 if dx != 0 and dy != 0 else 1
                neighbors.append(((nx, ny), cost))
        return neighbors
    
    def cost(node1, node2):
        x1, y1 = node1
        x2, y2 = node2
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        if dx > 0 and dy > 0:
            return 1.414
        return 1
    
    open_set = []
    g_score = {start: 0}
    rhs_score = {start: 0}
    came_from = {}
    
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    
    def calculate_key(node):
        min_g_rhs = min(g_score.get(node, float('inf')), rhs_score.get(node, float('inf')))
        return (min_g_rhs + heuristic(node, goal), min_g_rhs)
    
    def update_vertex(node):
        if node != goal:
            min_cost = float('inf')
            best_neighbor = None
            for neighbor, cost_val in get_neighbors(node):
                total = g_score.get(neighbor, float('inf')) + cost_val
                if total < min_cost:
                    min_cost = total
                    best_neighbor = neighbor
            rhs_score[node] = min_cost
            if best_neighbor:
                came_from[node] = best_neighbor
        
        if node in open_set:
            open_set[:] = [item for item in open_set if item[2] != node]
            heapq.heapify(open_set)
        
        if g_score.get(node, float('inf')) != rhs_score.get(node, float('inf')):
            key = calculate_key(node)
            heapq.heappush(open_set, (key[0], key[1], node))
    
    def compute_shortest_path():
        while open_set and (open_set[0][0] < calculate_key(goal)[0] or 
                           g_score.get(goal, float('inf')) != rhs_score.get(goal, float('inf'))):
            _, _, current = heapq.heappop(open_set)
            
            if g_score.get(current, float('inf')) > rhs_score.get(current, float('inf')):
                g_score[current] = rhs_score.get(current, float('inf'))
                for neighbor, _ in get_neighbors(current):
                    update_vertex(neighbor)
            else:
                g_score[current] = float('inf')
                for neighbor, _ in get_neighbors(current) + [(current, 0)]:
                    update_vertex(neighbor)
    
    update_vertex(goal)
    compute_shortest_path()
    
    if g_score.get(goal, float('inf')) == float('inf'):
        return [], None
    
    path = []
    current = start
    while current != goal:
        path.append(current)
        if current not in came_from:
            break
        current = came_from[current]
    path.append(goal)
    
    return path, g_score.get(goal, float('inf'))