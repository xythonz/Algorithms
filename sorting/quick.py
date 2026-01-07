def sort(unsorted):
    """Chooses a pivot and partitions the other elements around it and applies this same process to both sides of the pivot."""
    if len(unsorted) <= 1:
        return {"sorted": unsorted}
    
    pivot = unsorted[len(unsorted) // 2]
    
    left = [x for x in unsorted if x < pivot]
    middle = [x for x in unsorted if x == pivot]
    right = [x for x in unsorted if x > pivot]
    
    left_sorted = sort(left)["sorted"]
    right_sorted = sort(right)["sorted"]
    
    return left_sorted + middle + right_sorted

timeComplexity = "O(n log n)"
spaceComplexity = "O(n)"
variantOf = ""