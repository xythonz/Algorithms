def sort(unsorted):
    """Builds a max-heap to repeatedly extract the largest element and place it at the end until the array is sorted."""
    
    arr = unsorted.copy()
    n = len(arr)
    
    for i in range(n // 2 - 1, -1, -1):
        root = i
        while True:
            largest = root
            left = 2 * root + 1
            right = 2 * root + 2
            
            if left < n and arr[left] > arr[largest]:
                largest = left
                
            if right < n and arr[right] > arr[largest]:
                largest = right
                
            if largest != root:
                arr[root], arr[largest] = arr[largest], arr[root]
                root = largest
            else:
                break
    
    result = [0] * n
    
    for i in range(n - 1, -1, -1):
        result[i] = arr[0]
        if i > 0:
            arr[0] = arr[i]
            
            root = 0
            while True:
                largest = root
                left = 2 * root + 1
                right = 2 * root + 2
                
                if left < i and arr[left] > arr[largest]:
                    largest = left
                    
                if right < i and arr[right] > arr[largest]:
                    largest = right
                    
                if largest != root:
                    arr[root], arr[largest] = arr[largest], arr[root]
                    root = largest
                else:
                    break
    
    return result

timeComplexity = "O(n log n)"
spaceComplexity = "O(n)"  # Now requires O(n) additional space for the copy and result
variantOf = ""