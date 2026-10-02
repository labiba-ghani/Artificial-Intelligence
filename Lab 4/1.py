class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        """Add an item to the top of the stack."""
        self.items.append(item)

    def pop(self):
        """Remove and return the top item. Raise IndexError if empty."""
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        return self.items.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("peek from an empty stack")
        return self.items[-1]

    def is_empty(self):
        """Check if the stack has no elements."""
        return len(self.items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self.items)

    def display(self):
        """Display the stack elements."""
        return self.items

# Example Usage
if __name__ == "__main__":
    s = Stack()
    s.push(10)
    s.push(20)
    s.push(30)
    print("Stack:", s.display())
    print("Popped item:", s.pop())
    print("Top element (peek):", s.peek())
    print("size of the stack:", s.size())
    print("Is stack empty?", s.is_empty())