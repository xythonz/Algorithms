
def sort(unsorted):
    """Creates sorted blocks and merges them to sort the entire list."""
    if len(unsorted) <= 1:
        return unsorted[:]
    
    res = []
    blocks = [[unsorted[0]]]

    for item in unsorted[1:]:
        placed = False
        for block in blocks:
            if item >= block[-1]:
                block.append(item)
                placed = True
                break
        if not placed:
            blocks.append([item])
    
    while blocks:
        min_block = min(blocks, key=lambda b: b[0])
        res.append(min_block.pop(0))
        if not min_block:
            blocks.remove(min_block)
    
    return res

timeComplexity = "O(n log k)"
spaceComplexity = "O(n)"
variantOf = "merge"