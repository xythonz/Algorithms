def sort(unsorted):
    """Swaps the first smallest to the first position then second smallest to the second position and so on."""
    res = unsorted[:]
    for i in range(len(res)-1):
        min_idx = i
        for j in range(i+1, len(res)):
            if res[j] < res[min_idx]:
                min_idx = j
        res[i], res[min_idx] = res[min_idx], res[i]
    return res

timeComplexity = "O(n²)"
spaceComplexity = "O(1)"
variantOf = ""