def sort(unsorted):
    """Sorts every item into a 'bucket' by least significant digit then empties all of them in sequence. Then the least significant digit moves e.g. 1s->10s->100s."""
    
    res = unsorted[:]
    max_num = max(res)
    
    max_digits = len(str(max_num))
    
    for digit_position in range(max_digits):
        buckets = [[] for _ in range(10)]
        
        divisor = 10 ** digit_position
        
        for num in res:
            digit = (num // divisor) % 10
            buckets[digit].append(num)
        
        res = []
        for bucket in buckets:
            for num in bucket:
                res.append(num)
    
    return res

timeComplexity = "O(nk)"
spaceComplexity = "O(n + k)"
variantOf = ""