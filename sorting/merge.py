def sort(unsorted):
    """Seperates list into individual elements then 'merges' them back together."""
    lists = [[num] for num in unsorted]

    while len(lists) > 1:
        merged_lists = []
        for i in range(0, len(lists), 2):
            if i + 1 < len(lists):
                left = lists[i]
                right = lists[i + 1]
                merged = []

                l_idx = r_idx = 0
                while l_idx < len(left) and r_idx < len(right):
                    if left[l_idx] < right[r_idx]:
                        merged.append(left[l_idx])
                        l_idx += 1
                    else:
                        merged.append(right[r_idx])
                        r_idx += 1
                
                merged.extend(left[l_idx:])
                merged.extend(right[r_idx:])
                
                merged_lists.append(merged)
            else:
                merged_lists.append(lists[i])
        
        lists = merged_lists
    
    return lists[0] if lists else []

timeComplexity = "O(n log n)"
spaceComplexity = "O(n)"
variantOf = ""

