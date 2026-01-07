def search(data, target):
    """Estimates the position of the target using interpolation and searches accordingly. Only works on a sorted list with uniformly distributed values."""
    low = 0
    high = len(data) - 1
    while low <= high and target >= data[low] and target <= data[high]:
        if low == high:
            if data[low] == target:
                return low
            return -1
        pos = low + int(((float(high - low) / (data[high] - data[low])) * (target - data[low])))
        if data[pos] == target:
            return pos
        elif data[pos] < target:
            low = pos + 1
        else:
            high = pos - 1
    return -1

timeComplexity = "O(log log n)"
spaceComplexity = "O(1)"