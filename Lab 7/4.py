
class Graph:

    def __init__(self):
        # self.graph = {} creates an empty dictionary inside the object g.
        self.graph = {}  

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []

        self.graph[u].append(v)

    def dls(self, start, goal, limit):
        stack = [(start, 0, [start])]

        while stack:
            node, depth, path = stack.pop()

            print("Visiting:", node)

            if node == goal:
                return path

            if depth < limit:
                for neighbor in reversed(
                    self.graph.get(node, [])
                ):
                    stack.append(
                        (neighbor, depth + 1, path + [neighbor])
                    )

        return None

    def ids(self, start, goal, max_depth):

        for limit in range(max_depth + 1):

            print("\nDepth Limit:", limit)

            result = self.dls(start, goal, limit)

            if result is not None:
                return result

        return None


g = Graph()

g.add_edge("A", "B")
g.add_edge("A", "F")
g.add_edge("A", "D")
g.add_edge("A", "E")

g.add_edge("B", "K")
g.add_edge("B", "J")
g.add_edge("K", "N")
g.add_edge("K", "M")

g.add_edge("D", "G")

g.add_edge("E", "C")
g.add_edge("E", "H")
g.add_edge("E", "I")
g.add_edge("I", "L")

path = g.ids("A", "L", 3)

if path:
    print("\nGoal found!")
    print("Path:", " -> ".join(path))
else:
    print("Goal not found!")
