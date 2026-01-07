def comb_sort(unsorted):
    """Comb Sort: gapped comparisons with shrink factor ~1.3."""
    n = len(unsorted)
    if n <= 1:
        return unsorted
    a = list(unsorted)
    gap = n
    shrink = 1.3
    swapped = True

    while gap > 1 or swapped:
        gap = int(gap / shrink)
        if gap < 1:
            gap = 1
        swapped = False
        for i in range(0, n - gap):
            if a[i] > a[i + gap]:
                a[i], a[i + gap] = a[i + gap], a[i]
                swapped = True
    return a

timeComplexity = "O(n log n)"
spaceComplexity = "O(n)"
variantOf = "bubble"