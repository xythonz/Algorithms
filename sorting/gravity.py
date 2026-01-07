def gravity_sort(arr):
    """Simulates beads falling under gravity to sort the array."""
    max_val = max(arr)
    n = len(arr)
    grid = [[0] * max_val for _ in range(n)]
    
    for i, val in enumerate(arr):
        for j in range(val):
            grid[i][j] = 1

    for j in range(max_val):
        bead_count = sum(grid[i][j] for i in range(n))
        
        for i in range(n):
            grid[i][j] = 0
            
        for i in range(n - bead_count, n):
            grid[i][j] = 1

    sorted_arr = [sum(row) for row in grid]
    return sorted_arr

timeComplexity = "O(n k)"
spaceComplexity = "O(n k)"
variantOf = "" 