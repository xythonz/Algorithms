def sort(unsorted):
    """Recursively sorts by dividing into 2/3 portions and sorting first, last, then first again."""
    a = list(unsorted)
    if len(a) <= 1:
        return a
    
    stack = [(0, len(a) - 1, 0)]  # (left, right, phase)
    
    while stack:
        left, right, phase = stack.pop()
        
        if a[left] > a[right]:
            a[left], a[right] = a[right], a[left]
        
        if left + 1 >= right:
            continue
        
        size = (right - left + 1) // 3
        
        if phase == 0:
            stack.append((left, right, 1))
            stack.append((left, right - size, 0))
        elif phase == 1:
            stack.append((left, right, 2))
            stack.append((left + size, right, 0))
        else:
            stack.append((left, right - size, 0))
    
    return a

timeComplexity = "O(n^2.71)"
spaceComplexity = "O(log n)"
variantOf = ""
