counter = 0

def worker():
    global counter
for _ in range(100000):
    counter += 1

threads = []

for _ in range(10):
    t = Thread(target=worker)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(counter)