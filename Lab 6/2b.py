#with path
def dfs(graph, start, goal):
    visited = set()
    stack = [(start, [start])]

    while stack:
        node, path = stack.pop()

        if node not in visited:
            print(node, end=" ")
            visited.add(node)

            if node == goal:
                print("\nGoal found!")
                print("Path:", " -> ".join(path))
                # The join() method combines the strings in the path list using " -> " as the separator.
                return

            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

    print("\nGoal not found!")


graph = {
    'A': ['B', 'F', 'D', 'E'],
    'B': ['K', 'J'],
    'K': ['N', 'M'],
    'N': [],
    'M': [],
    'J': [],
    'F': [],
    'D': ['G'],
    'G': [],
    'E': ['C', 'H', 'I'],
    'C': [],
    'H': [],
    'I': ['L'],
    'L': []
}

dfs(graph, 'A', 'G')
