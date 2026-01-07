def sort(unsorted):
    """Counts the frequency of each value, then rebuilds the sorted array based on those counts."""
    minimum = min(unsorted)
    maximum = max(unsorted)
    
    bucket_size = maximum - minimum + 1
    buckets = [0] * bucket_size
    
    for item in unsorted:
        buckets[item - minimum] += 1
    
    res = []
    for i in range(len(buckets)):
        count = buckets[i]
        if count > 0:
            res.extend([i + minimum] * count)
    
    return res

timeComplexity = "O(n + k)"
spaceComplexity = "O(k)"
variantOf = ""