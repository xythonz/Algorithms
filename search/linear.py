def search(data, target):
    """Checks each element in the list until the target is found."""
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1

timeComplexity = "O(n)"
spaceComplexity = "O(1)"