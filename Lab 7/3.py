# Iterative Deepening Search

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


def ids(start, goal, max_depth):

    for limit in range(max_depth + 1):

        print("\nDepth Limit:", limit)

        result = dls(start, goal, limit)

        if result is not None:
            return result

    return None


path = ids("A", "G", 3)

if path:
    print("\nGoal found!")
    print("Path:", " -> ".join(path))
else:
    print("Goal not found!")

# Why do we write max_depth + 1?
# Because Python's range() excludes the ending value. Adding 1 ensures that the maximum depth is included.
# range(3 + 1) -> 0 1 2 3