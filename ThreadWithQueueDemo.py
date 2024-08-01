import threading
import queue

# Create a queue to share information between threads
data_queue = queue.Queue()

# Function to be executed by each thread
def worker(thread_id):
    while True:
        # Get data from the queue
        data = data_queue.get()

        # Process the data (e.g., print it)
        print(f"Thread {thread_id}: {data}")

        # Signal that the task is done
        data_queue.task_done()

# Create multiple threads
threads = []
for i in range(3):
    thread = threading.Thread(target=worker, args=(i,))
    thread.daemon = True  # Allow the main thread to exit even if threads are still running
    thread.start()
    threads.append(thread)

# Add data to the queue
for i in range(10):
    data_queue.put(f"Data {i}")

# Wait for all tasks to be completed
data_queue.join()

print("All tasks completed.")
