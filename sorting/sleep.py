import time
import threading

def sort(unsorted):
    res = []
    lock = threading.Lock()
    for num in unsorted:
        t = threading.Thread(target=lambda n: (time.sleep(n * 0.01), lock.acquire(), res.append(n), lock.release()), args=(num,))
        t.start()
    
    time.sleep(max(unsorted) * 0.01 + 0.1)
    return res

timeComplexity = "O(n + k)"
spaceComplexity = "O(n)"