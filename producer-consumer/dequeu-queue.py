from collections import deque
import threading
import random
import time
import sys

class BlockingQueue:

    def __init__(self):
        self.q = deque()
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)


    def put(self, item):
        with self.lock:
            self.q.append(item)
            self.condition.notify()

    def get(self):
        with self.lock:
            while len(self.q) == 0:
                self.condition.wait()
            return self.q.popleft()

def produce(shared_q, num_consumers):
    packet_id = 1
    total_packets = 10
    while packet_id <= total_packets:
        delay = random.uniform(0.1,1.0)
        print(f"Random sleep period: {delay}")
        time.sleep(delay)
        shared_q.put(f"packet_{packet_id}")
        packet_id += 1
    
    for _ in range(num_consumers):
        shared_q.put(None)  # to signal the end
    print("[Producer] Finished packets generation")


def consume(packet_queue, consumer_id):
    while True:
        packet = packet_queue.get()

        if packet is None:
            break

        print(f"  [Consumer-{consumer_id}] Processing: {packet}...")
        time.sleep(random.uniform(2.0, 3.0)) 
        print(f"  [Consumer-{consumer_id}] Finished processing: {packet}")

        # Signal to the queue that the job is done
        #packet_queue.task_done()
    
    print(f"[Consumer-{consumer_id}] No more packets. Shutting down.")


def main():
    NUM_CONSUMERS = 3
    shared_q = BlockingQueue()

    producer = threading.Thread(target=produce, args=(shared_q, NUM_CONSUMERS))
    producer.start()

    consumers = []
    for i in range(NUM_CONSUMERS):
        consumer = threading.Thread(target=consume, args=(shared_q, i))
        consumer.start()
        consumers.append(consumer)
    
    

    producer.join()
    for c in consumers:
        c.join()

    print("Finished producer-consumer main thread")


if __name__ == "__main__":
    sys.exit(main())