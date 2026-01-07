def sort(unsorted):
    """Recursively builds sorted sublists and merges them to sort the entire list."""
    def merge(sorted1, sorted2):
        result = []
        i = j = 0
        while i < len(sorted1) and j < len(sorted2):
            if sorted1[i] < sorted2[j]:
                result.append(sorted1[i])
                i += 1
            else:
                result.append(sorted2[j])
                j += 1
        result.extend(sorted1[i:])
        result.extend(sorted2[j:])
        return result
    res = []
    while unsorted:
        sublist = [unsorted.pop(0)]
        i = 0
        while i < len(unsorted):
            if unsorted[i] >= sublist[-1]:
                sublist.append(unsorted.pop(i))
            else:
                i += 1
        res = merge(res, sublist)
    return res

timeComplexity = "O(n log n)"
spaceComplexity = "O(n)"
variantOf = "merge"

print(sort([34, 7, 23, 32, 5, 62]))  