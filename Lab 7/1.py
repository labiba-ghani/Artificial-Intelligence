#iterative approch
#depth limit approch (include depth limit)
def dls(start, goal, limit):

    stack = [(start, 0, [start])]

    while stack:
        node, depth, path = stack.pop()

        print("Visiting:", node)

        if node == goal:
            return path

        if depth < limit:
            for neighbor in reversed(graph[node]):
                stack.append(
                    (neighbor, depth + 1, path + [neighbor])
                )

    return None


graph = {
    "A": ["B", "F", "D", "E"],
    "B": ["K", "J"],
    "F": [],
    "D": ["G"],
    "E": ["C", "H", "I"],
    "K": ["N", "M"],
    "J": [],
    "G": [],
    "C": [],
    "H": [],
    "I": ["L"],
    "N": [],
    "M": [],
    "L": []
}
result = dls("A", "G", 2)

if result:
    print("Goal found!")
    print("Path:", " -> ".join(result))
else:
    print("Goal not found!")
