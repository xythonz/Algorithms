# Floyd-Warshall Algorithm
def pathfind(graph, start, goal, positions):
    # Floyd-Warshall computes all-pairs shortest paths
    # It doesn't use heuristics, but we accept positions for consistency
    # Get all nodes
    nodes = list(graph.keys())
    n = len(nodes)

    # Create node to index mapping
    node_to_idx = {node: i for i, node in enumerate(nodes)}

    # Initialize distance and next matrices
    dist = [[float('inf')] * n for _ in range(n)]
    next_node = [[None] * n for _ in range(n)]

    # Set diagonal to 0
    for i in range(n):
        dist[i][i] = 0

    # Set edges
    for u in graph:
        u_idx = node_to_idx[u]
        for v, weight in graph[u].items():
            v_idx = node_to_idx[v]
            dist[u_idx][v_idx] = weight
            next_node[u_idx][v_idx] = v

    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next_node[i][j] = next_node[i][k]

    # Reconstruct path
    start_idx = node_to_idx[start]
    goal_idx = node_to_idx[goal]

    if dist[start_idx][goal_idx] == float('inf'):
        return [], None

    path = [start]
    current_idx = start_idx
    while current_idx != goal_idx:
        current_idx = node_to_idx[next_node[current_idx][goal_idx]]
        path.append(nodes[current_idx])

    return path, dist[start_idx][goal_idx]