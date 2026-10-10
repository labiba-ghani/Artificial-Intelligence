from collections import deque

class Graph:

    def __init__(self):
        self.graph = {}

    def add_edge(self, node, neighbors):
        self.graph[node] = neighbors

    def bfs(self, start):
        visited = set()
        queue = deque([start])
        visited.add(start)

        while queue:
            node = queue.popleft()
            print(node, end=" ")

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

    def bfs_with_goal(self, start, goal):
        visited = set()
        queue = deque([(start, [start])])
        visited.add(start)

        while queue:
            node, path = queue.popleft()
            print(node, end=" ")

            if node == goal:
                print("\nGoal found!")
                print("Path:", " -> ".join(path))
                return

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        print("\nGoal not found.")


g1 = Graph()

g1.add_edge(0, [1, 4])
g1.add_edge(1, [0, 4, 3, 2])
g1.add_edge(2, [1, 3])
g1.add_edge(3, [1, 2, 4])
g1.add_edge(4, [0, 1, 3])

print("Task 1 BFS:")
g1.bfs(0)


g2 = Graph()

g2.add_edge('A', ['B', 'F', 'D', 'E'])
g2.add_edge('B', ['K', 'J'])
g2.add_edge('F', [])
g2.add_edge('D', ['G'])
g2.add_edge('E', ['C', 'H', 'I'])
g2.add_edge('K', ['N', 'M'])
g2.add_edge('J', [])
g2.add_edge('G', [])
g2.add_edge('C', [])
g2.add_edge('H', [])
g2.add_edge('I', ['L'])
g2.add_edge('N', [])
g2.add_edge('M', [])
g2.add_edge('L', [])

print("\n\nTask 2 BFS:")
g2.bfs_with_goal('A', 'Z')