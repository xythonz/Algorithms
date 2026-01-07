def sort(unsorted):
    "Inserts the current item, comparing it to all previous items in the list until the correct position is found."
    res = unsorted[:]
    for i in range(1, len(res)):
        key = res[i]
        j = i - 1
        while j >= 0 and res[j] > key:
            res[j + 1] = res[j]
            j -= 1
        res[j + 1] = key
    return res

timeComplexity = "O(n²)"
spaceComplexity = "O(1)"
variantOf = ""