def sort(unsorted):
    """Optimizes insertion sort by pre-sorting distant elements with decreasing gaps for fewer final moves."""
    res = unsorted[:]
    n = len(res)
    gap = n // 2 
    
    while gap > 0:
        for i in range(gap, n):
            temp = res[i]
            j = i
            
            while j >= gap and res[j - gap] > temp:
                res[j] = res[j - gap]
                j -= gap
            
            res[j] = temp
        
        gap //= 2 
    return res

timeComplexity = "O(n (log n)²)"
spaceComplexity = "O(1)"
variantOf = "insertion"