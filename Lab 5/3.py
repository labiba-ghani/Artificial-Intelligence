# Class used to store an item and its priority
class Priority:

    def __init__(self, item, priority):
        self.item = item
        self.priority = priority


# Priority Queue class
class PriorityQueue:

    def __init__(self):
        # Create an empty queue
        self.queue = []

    # Add an item to the queue
    def enqueue(self, item, priority):

        # Create a Priority object
        new_item = Priority(item, priority)

        # Add the object to the queue
        self.queue.append(new_item)

    # Remove the highest-priority item
    def dequeue(self):

        # Check if queue is empty
        if len(self.queue) == 0:
            print("Queue is empty")
            return

        # Initially assume first item has highest priority
        highest = 0

        # Search for the item with highest priority
        for i in range(1, len(self.queue)):

            # Smaller number means higher priority
            if self.queue[i].priority < self.queue[highest].priority:
                highest = i

        # Remove and return highest-priority item
        item = self.queue.pop(highest)

        return item

    # Display the queue
    def display(self):

        for item in self.queue:
            print(item.item, "Priority:", item.priority)


# Create priority queue
pq = PriorityQueue()

# Insert items
pq.enqueue("A", 3)
pq.enqueue("B", 1)
pq.enqueue("C", 2)

print("Priority Queue:")
pq.display()

# Remove items according to priority
print("\nRemoving items:")

while len(pq.queue) > 0:

    item = pq.dequeue()

    print(item.item, "Priority:", item.priority)