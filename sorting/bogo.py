import random

def sort(unsorted):
    """Randomizes list until sorted."""
    res = unsorted[:]
    
    while True:
        for i in range(len(res) - 1):
            if res[i] > res[i + 1]:
                random.shuffle(res)
                break
        else:
            break
    
    return res

timeComplexity = "O((n+1)!)"
spaceComplexity = "O(1)"
variantOf = ""