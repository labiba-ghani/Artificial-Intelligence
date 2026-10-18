#recursive approch 

def dls(node, goal, limit):

    print("Visiting:", node)

    if node == goal:
        return True

    if limit == 0:
        return False

    for neighbor in graph[node]:
        if dls(neighbor, goal, limit - 1):
            return True

    return False

# First, represent the tree using an adjacency list.
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
else:
    print("Goal not found!")
