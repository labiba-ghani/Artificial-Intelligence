
class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, node, neighbors):
        self.graph[node] = neighbors

    def dfs(self, start):
        visited = set()
        stack = [start]

        print("DFS Traversal:", end=" ")

        while stack:
            node = stack.pop()

            if node not in visited:
                print(node, end=" ")
                visited.add(node)

                for neighbor in reversed(self.graph[node]):
                    if neighbor not in visited:
                        stack.append(neighbor)

        print()

    def dfs_with_goal(self, start, goal):
        visited = set()
        stack = [(start, [start])]

        print("DFS Traversal:", end=" ")

        while stack:
            node, path = stack.pop()

            if node not in visited:
                print(node, end=" ")
                visited.add(node)

                if node == goal:
                    print("\nGoal Found!")
                    print("Path:", " -> ".join(path))
                    return

                for neighbor in reversed(self.graph[node]):
                    if neighbor not in visited:
                        stack.append((neighbor, path + [neighbor]))

        print("\nGoal Not Found!")


g = Graph()

g.add_edge('A', ['B', 'F', 'D', 'E'])
g.add_edge('B', ['K', 'J'])
g.add_edge('K', ['N', 'M'])
g.add_edge('N', [])
g.add_edge('M', [])
g.add_edge('J', [])
g.add_edge('F', [])
g.add_edge('D', ['G'])
g.add_edge('G', [])
g.add_edge('E', ['C', 'H', 'I'])
g.add_edge('C', [])
g.add_edge('H', [])
g.add_edge('I', ['L'])
g.add_edge('L', [])

g.dfs('A')
print()
g.dfs_with_goal('A', 'L')

# class Graph: defines a class.
# __init__() is the constructor, which runs automatically when we create an object.
# self refers to the current object.
# self.graph = {} creates an empty dictionary to store the graph.