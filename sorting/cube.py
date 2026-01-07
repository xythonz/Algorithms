def sort(unsorted):
    """Sorts by creating cubes of sorted sublists and merging them."""
    def merge(sorted1, sorted2):
        res = []
        i = j = 0
        while i < len(sorted1) and j < len(sorted2):
            if sorted1[i] < sorted2[j]:
                res.append(sorted1[i])
                i += 1
            else:
                res.append(sorted2[j])
                j += 1
        res.extend(sorted1[i:])
        res.extend(sorted2[j:])
        return res

    def strand_sort(lst):
        if not lst:
            return []
        sublist = [lst.pop(0)]
        i = 0
        while i < len(lst):
            if lst[i] >= sublist[-1]:
                sublist.append(lst.pop(i))
            else:
                i += 1
        return merge(sublist, strand_sort(lst))

    return strand_sort(list(unsorted))

timeComplexity = "O(n log n)"
spaceComplexity = "O(n)"