def search(data, target):
    """Halves the list each time to find the target efficiently. Only works on a sorted list."""
    low = 0
    high = len(data) - 1
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