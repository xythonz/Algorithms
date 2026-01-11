
def search(data, target):
    """Searches for the target by jumping ahead by fixed steps and then performing a linear search within the identified block. Only works on a sorted list."""
    step = int(len(data) ** 0.5)
    prev = 0
    while prev < len(data) and data[min(step, len(data)) - 1] < target:
        prev = step
        step += int(len(data) ** 0.5)
        if prev >= len(data):
            return -1
    for i in range(prev, min(step, len(data))):
        if data[i] == target:
            return i
    return -1

timeComplexity = "O(√n)"
spaceComplexity = "O(1)"