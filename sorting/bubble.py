def sort(unsorted):
    """Iterates through the list, comparing it to the next item. Repeats until sorted."""
    res = unsorted[:]
    while True:
        comparisons = False
        for i in range(len(res)-1):
            if res[i+1] < res[i]:
                comparisons = True
                res[i], res[i+1] = res[i+1], res[i]
        if not comparisons:
            break
    return res

timeComplexity = "O(n²)"
spaceComplexity = "O(1)"
variantOf = ""