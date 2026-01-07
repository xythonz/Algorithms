def sort(unsorted):
    """Distributes elements into 'pigeonholes' and then collects them in order."""
    if not unsorted:
        return []

    min_val = min(unsorted)
    max_val = max(unsorted)
    size = max_val - min_val + 1

    holes = [[] for _ in range(size)]

    for num in unsorted:
        holes[num - min_val].append(num)

    res = []
    for hole in holes:
        res.extend(hole)

    return res

timeComplexity = "O(n + k)"
spaceComplexity = "O(n + k)"
variantOf = ""