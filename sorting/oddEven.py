def sort(unsorted):
    """Sorts the list by swapping odd and even indexed pairs in alternating passes."""
    res = unsorted[:]
    n = len(res)
    swapped = False
    while True:
        swapped = False
        for i in range(1, n-1, 2):
            if res[i] > res[i+1]:
                res[i], res[i+1] = res[i+1], res[i]
                swapped = True
        for i in range(0, n-1, 2):
            if res[i] > res[i+1]:
                res[i], res[i+1] = res[i+1], res[i]
                swapped = True
        if not swapped:
            break
    return res

timeComplexity = "O(n²)"
spaceComplexity = "O(1)"
variantOf = "bubble"