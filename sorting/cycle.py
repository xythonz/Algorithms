def sort(unsorted):
    """Find each element's final position by counting smaller items, then rotate it into place through successive swaps until sorted."""
    res = unsorted[:]
    
    for start in range(len(res) - 1):
        current_item = res[start]
        
        position = start
        for i in range(start + 1, len(res)):
            if res[i] < current_item:
                position += 1
        
        if position == start:
            continue
        
        while current_item == res[position]:
            position += 1
        
        res[position], current_item = current_item, res[position]
        
        while position != start:
            position = start
            for i in range(start + 1, len(res)):
                if res[i] < current_item:
                    position += 1
            
            while current_item == res[position]:
                position += 1
            
            res[position], current_item = current_item, res[position]
    
    return res

timeComplexity = "O(n²)"
spaceComplexity = "O(1)"
variantOf = "selection"