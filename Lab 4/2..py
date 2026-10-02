from collections import deque

# Double-Ended Queue

# It is a special Python data structure that allows us to efficiently add and remove elements from both ends.
class Queue:
    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        """Add an element to the rear of the queue."""
        self.items.append(item)

    def dequeue(self):
        """Remove and return the front element. Raise IndexError if empty."""
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        return self.items.popleft()

    def peek(self):
        """Return the front element without removing it."""
        if self.is_empty():
            raise IndexError("peek from an empty queue")
        return self.items[0]

    def is_empty(self):
        """Check if the queue is empty."""
        return len(self.items) == 0

    def size(self):
        """Return the number of elements in the queue."""
        return len(self.items)

    def display(self):
        """Display the elements currently in the queue."""
        return list(self.items)


# Example Usage
if __name__ == "__main__":
    q = Queue()
    q.enqueue("A")
    q.enqueue("B")
    q.enqueue("C")
    print("Queue:", q.display())
    print("Dequeued item:", q.dequeue())
    print("Front element (peek):", q.peek())
    print("size of the stack:", q.size())
    print("Queue size:", q.size())