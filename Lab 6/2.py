#without path
def dfs(graph, start, goal):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()

        if node not in visited:
            print(node, end=" ")
            visited.add(node)

            if node == goal:
                print("\nGoal found!")
                return

            for neighbor in reversed(graph[node]):
                if neighbor not in visited:
                    stack.append(neighbor)

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
