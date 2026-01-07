def sort(unsorted):
    if not unsorted:
        return []
    
    res = unsorted[:]
    n = len(res)
    MIN_MERGE = 32
    
    n_copy = n
    r = 0
    while n_copy >= MIN_MERGE:
        r |= n_copy & 1
        n_copy >>= 1
    min_run = n_copy + r
    
    start = 0
    while start < n:
        end = min(start + min_run, n)
        i = start + 1
        while i < end:
            key = res[i]
            j = i - 1
            while j >= start and res[j] > key:
                res[j + 1] = res[j]
                j -= 1
            res[j + 1] = key
            i += 1
        start += min_run
    
    size = min_run
    while size < n:
        left = 0
        while left < n:
            mid = min(n, left + size)
            right = min(n, left + 2 * size)
            if mid < right:
                len1 = mid - left
                len2 = right - mid
                left_unsorted = [0] * len1
                right_unsorted = [0] * len2
                x = 0
                while x < len1:
                    left_unsorted[x] = res[left + x]
                    x += 1
                y = 0
                while y < len2:
                    right_unsorted[y] = res[mid + y]
                    y += 1
                i = 0
                j = 0
                k = left
                while i < len1 and j < len2:
                    if left_unsorted[i] <= right_unsorted[j]:
                        res[k] = left_unsorted[i]
                        i += 1
                    else:
                        res[k] = right_unsorted[j]
                        j += 1
                    k += 1
                while i < len1:
                    res[k] = left_unsorted[i]
                    i += 1
                    k += 1
                while j < len2:
                    res[k] = right_unsorted[j]
                    j += 1
                    k += 1
            left += 2 * size
        size = 2 * size
    
    return res

timeComplexity = "O(n log n)"
spaceComplexity = "O(n)"
variantOf = "merge and insertion"