#flash sort
def sort(unsorted):
    """Distributes elements into classes and then sorts within those classes."""
    n = len(unsorted)
    m = int(0.43 * n)
    if m < 2:
        m = 2

    min_val = min(unsorted)
    max_val = max(unsorted)

    if min_val == max_val:
        return unsorted[:]

    class_counts = [0] * m
    for num in unsorted:
        class_idx = int((m - 1) * (num - min_val) / (max_val - min_val))
        class_counts[class_idx] += 1

    for i in range(1, m):
        class_counts[i] += class_counts[i - 1]

    res = unsorted[:]
    n_moved = 0
    j = 0
    k = m - 1

    while n_moved < n:
        while j >= class_counts[k]:
            j += 1
            k = int((m - 1) * (res[j] - min_val) / (max_val - min_val))

        evicted = res[j]
        while j < class_counts[k]:
            class_idx = int((m - 1) * (evicted - min_val) / (max_val - min_val))
            dest_idx = class_counts[class_idx] - 1
            class_counts[class_idx] -= 1

            res[dest_idx], evicted = evicted, res[dest_idx]
            n_moved += 1

    start = 0
    for i in range(m):
        end = class_counts[i] if i < m - 1 else n
        for j in range(start + 1, end):
            key = res[j]
            k = j - 1
            while k >= start and res[k] > key:
                res[k + 1] = res[k]
                k -= 1
            res[k + 1] = key
        start = end

    return res

timeComplexity = "O(n)"
spaceComplexity = "O(m)"
variantOf = "bucket"