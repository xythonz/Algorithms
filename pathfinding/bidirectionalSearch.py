# Bidirectional Search Algorithm using A* from both directions
import heapq
import math

def pathfind(graph, start, goal, positions):
    def euclidean_distance(a, b):
        """Calculate Euclidean distance between two nodes using their positions"""
        x1, y1 = positions[a]
        x2, y2 = positions[b]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    if start == goal:
        return [start], 0

    # Forward search from start (using A* towards goal)
    forward_pq = [(euclidean_distance(start, goal), 0, start)]
    forward_visited = {}
    forward_dist = {start: 0}
    forward_parent = {start: None}

    # Backward search from goal (using A* towards start)
    backward_pq = [(euclidean_distance(goal, start), 0, goal)]
    backward_visited = {}
    backward_dist = {goal: 0}
    backward_parent = {goal: None}

    best_path_length = float('inf')
    meeting_node = None

    while forward_pq or backward_pq:
        # Expand from forward direction
        if forward_pq:
            _, f_g_score, f_node = heapq.heappop(forward_pq)

            if f_node in forward_visited:
                continue

            forward_visited[f_node] = True

            # Check if we can connect to backward search
            if f_node in backward_visited:
                path_length = forward_dist[f_node] + backward_dist[f_node]
                if path_length < best_path_length:
                    best_path_length = path_length
                    meeting_node = f_node

            # Early termination: if current g-score exceeds best path, stop forward search
            if f_g_score > best_path_length:
                forward_pq = []
            else:
                # Expand neighbors
                for neighbor, weight in graph.get(f_node, {}).items():
                    new_dist = forward_dist[f_node] + weight
                    if neighbor not in forward_visited and (neighbor not in forward_dist or new_dist < forward_dist[neighbor]):
                        forward_dist[neighbor] = new_dist
                        forward_parent[neighbor] = f_node
                        f_score = new_dist + euclidean_distance(neighbor, goal)
                        heapq.heappush(forward_pq, (f_score, new_dist, neighbor))

        # Expand from backward direction
        if backward_pq:
            _, b_g_score, b_node = heapq.heappop(backward_pq)

            if b_node in backward_visited:
                continue

            backward_visited[b_node] = True

            # Check if we can connect to forward search
            if b_node in forward_visited:
                path_length = forward_dist[b_node] + backward_dist[b_node]
                if path_length < best_path_length:
                    best_path_length = path_length
                    meeting_node = b_node

            # Early termination: if current g-score exceeds best path, stop backward search
            if b_g_score > best_path_length:
                backward_pq = []
            else:
                # Expand neighbors
                for neighbor, weight in graph.get(b_node, {}).items():
                    new_dist = backward_dist[b_node] + weight
                    if neighbor not in backward_visited and (neighbor not in backward_dist or new_dist < backward_dist[neighbor]):
                        backward_dist[neighbor] = new_dist
                        backward_parent[neighbor] = b_node
                        f_score = new_dist + euclidean_distance(neighbor, start)
                        heapq.heappush(backward_pq, (f_score, new_dist, neighbor))

    # No path found
    if meeting_node is None:
        return [], None

    # Reconstruct path from start to meeting point
    path_forward = []
    current = meeting_node
    while current is not None:
        path_forward.append(current)
        current = forward_parent[current]
    path_forward.reverse()

    # Reconstruct path from meeting point to goal
    path_backward = []
    current = backward_parent[meeting_node]
    while current is not None:
        path_backward.append(current)
        current = backward_parent[current]

    # Combine paths
    full_path = path_forward + path_backward

    return full_path, best_path_length