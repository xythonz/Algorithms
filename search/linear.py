def search(data, target):
    """Checks each element in the list until the target is found."""
    for element in data:
        if element == target:
            return True
    return False

timeComplexity = "O(n)"
spaceComplexity = "O(1)"