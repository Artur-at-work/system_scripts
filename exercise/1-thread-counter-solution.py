import threading
import multiprocessing
import time

counter = 0

start = time.perf_counter()

def worker():
    global counter
    for _ in range(100000000):
        counter += 1

threads = []

for _ in range(10):
    t = multiprocessing.Process(target=worker)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

elapsed = time.perf_counter() - start
print(counter)
print(f"Elapsed time: {elapsed:.4f}s")