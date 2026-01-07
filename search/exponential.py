def search(data, target):
    """Searches for the target by first finding a range using exponential growth, then performing binary search within that range. Only works on a sorted list."""
    if len(data) == 0:
        return False
    if data[0] == target:
        return True

    index = 1
    while index < len(data) and data[index] <= target:
        index *= 2

    low = index // 2
    high = min(index, len(data) - 1)

    while low <= high:
        mid = (low + high) // 2
        if data[mid] == target:
            return True
        elif data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return False

timeComplexity = "O(log n)"
spaceComplexity = "O(1)"