from collections import deque

def bfs(graph, start, goal):
    # Stores nodes that have already been discovered
    visited = set()
    # Create queue with starting node
    queue = deque([start])
    visited.add(start)

    while queue:

        node = queue.popleft()

  
        print(node, end=" ")

        # Check whether current node is our goal
        if node == goal:
            print("\nGoal found!")
            return

        # Check all neighbors of current node
        for neighbor in graph[node]:

            
            if neighbor not in visited:

                
                visited.add(neighbor)

                
                queue.append(neighbor)

    # If queue becomes empty without finding goal
    print("\nGoal not found.")

# Adjacency list 
graph = {
    'A': ['B', 'F', 'D', 'E'],
    'B': ['K', 'J'],
    'F': [],
    'D': ['G'],
    'E': ['C', 'H', 'I'],
    'K': ['N', 'M'],
    'J': [],
    'G': [],
    'C': [],
    'H': [],
    'I': ['L'],
    'N': [],
    'M': [],
    'L': []
}

bfs(graph, 'A', 'G')