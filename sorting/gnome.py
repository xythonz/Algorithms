def sort(unsorted):
    """Compares adjacent elements and if incorrect, swaps and moves back one position."""
    length = len(unsorted)
    res = unsorted[:]
    i = 1
    while i < length:
        if res[i] >= res[i-1]:
            i += 1
        else:
            res[i], res[i-1] = res[i-1], res[i]
            if i > 1:
                i -= 1
            else:
                i += 1
    return res

timeComplexity = "O(n^2)"
spaceComplexity = "O(1)"
variantOf = "insertion"