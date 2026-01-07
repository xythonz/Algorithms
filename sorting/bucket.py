def sort(unsorted):
    """Divides elements into buckets based on value ranges, sorts each bucket, then concatenates results."""
    if len(unsorted) == 0:
        return unsorted
    
    minimum = min(unsorted)
    maximum = max(unsorted)
    
    bucket_count = len(unsorted)
    bucket_range = (maximum - minimum) / bucket_count
    
    buckets = [[] for _ in range(bucket_count)]
    
    for item in unsorted:
        if item == maximum:
            buckets[bucket_count - 1].append(item)
        else:
            index = int((item - minimum) / bucket_range)
            buckets[index].append(item)
    
    res = []
    for bucket in buckets:
        res.extend(sorted(bucket))
    
    return res

timeComplexity = "O(n + k) average, O(n²) worst case"
spaceComplexity = "O(n + k)"
variantOf = ""