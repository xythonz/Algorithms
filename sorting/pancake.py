def sort(unsorted):
    """Flips elements from the start up to the maximum unsorted element repeatedly to sort the list."""
    res = unsorted[:]
    n = len(res)
    while n > 1:
        max_index = res.index(max(res[:n]))
        if max_index != n - 1:
            res[:max_index+1] = reversed(res[:max_index+1])
            res[:n] = reversed(res[:n])
        n -= 1
    return res

timeComplexity = "O(n²)"
spaceComplexity = "O(1)"
variantOf = "selection"