import sys
import threading
import queue
import time
import random

packet_queue = queue.Queue(maxsize=10)

def produce():
    packet_id = 1
    total_packets = 10
    while packet_id <= total_packets:
        delay = random.uniform(1.0,2.0)
        print(f"Random sleep period: {delay}")
        time.sleep(delay)
        packet_queue.put(f"packet_{packet_id}")
        packet_id += 1
    
    packet_queue.put(None)  # to signal the end
    print("[Producer] Finished packets generation")


    

def consume():
    while True:
        packet = packet_queue.get()

        if packet is None:
            break

        print(f"  [Consumer] Processing: {packet}...")
        time.sleep(random.uniform(0.5, 1.2)) 
        print(f"  [Consumer] Finished processing: {packet}")

        # Signal to the queue that the job is done
        packet_queue.task_done()
    
    print("[Consumer] No more packets. Shutting down.")


def main():
    
    producer_thread = threading.Thread(target=produce)
    consumer_thread = threading.Thread(target=consume)


    # Start the threads
    producer_thread.start()
    consumer_thread.start()
    # Wait for both threads to finish completely before exiting the program
    producer_thread.join()
    consumer_thread.join()

    print("\nSystem gracefully shut down.")


if __name__ == "__main__":
    sys.exit(main())