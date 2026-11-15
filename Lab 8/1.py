
# Task 1: Greedy Best-First Search

# Define the graph using an adjacency list
graph = {
    "Arad": ["Zerind", "Sibiu", "Timisoara"],
    "Zerind": ["Arad", "Oradea"],
    "Sibiu": ["Arad", "Oradea", "Fagaras", "Rimnicu Vilcea"],
    "Timisoara": ["Arad", "Lugoj"],
    "Lugoj": ["Timisoara", "Mehadia"],
    "Mehadia": ["Lugoj", "Drobeta"],
    "Drobeta": ["Mehadia", "Craiova"],
    "Craiova": ["Drobeta", "Rimnicu Vilcea", "Pitesti"],
    "Oradea": ["Zerind", "Sibiu"],
    "Fagaras": ["Sibiu", "Bucharest"],
    "Rimnicu Vilcea": ["Sibiu", "Craiova", "Pitesti"],
    "Pitesti": ["Rimnicu Vilcea", "Craiova", "Bucharest"],
    "Bucharest": ["Fagaras", "Pitesti", "Giurgiu", "Urziceni"],
    "Giurgiu": ["Bucharest"],
    "Urziceni": ["Bucharest", "Hirsova", "Vaslui"],
    "Hirsova": ["Urziceni", "Eforie"],
    "Eforie": ["Hirsova"],
    "Vaslui": ["Urziceni", "Iasi"],
    "Iasi": ["Vaslui", "Neamt"],
    "Neamt": ["Iasi"]
}

# Heuristic values: straight-line distance to Bucharest
heuristic = {
    "Arad": 366,
    "Bucharest": 0,
    "Craiova": 160,
    "Drobeta": 242,
    "Eforie": 161,
    "Fagaras": 176,
    "Giurgiu": 77,
    "Hirsova": 151,
    "Iasi": 226,
    "Lugoj": 244,
    "Mehadia": 241,
    "Neamt": 234,
    "Oradea": 380,
    "Pitesti": 100,
    "Rimnicu Vilcea": 193,
    "Sibiu": 253,
    "Timisoara": 329,
    "Urziceni": 80,
    "Vaslui": 199,
    "Zerind": 374
}

# Greedy Best-First Search algorithm
def greedy_best_first_search(graph, heuristic, start, goal):

    open_list = [(start, [start])]
    visited = set()

    while open_list:

        # Select the node with the lowest heuristic value
        open_list.sort(key=lambda x: heuristic[x[0]])

        current, path = open_list.pop(0)

        # Skip already visited nodes
        if current in visited:
            continue

        print("Visiting:", current)

        # Check whether the goal has been reached
        if current == goal:
            return path

        visited.add(current)

        # Explore neighbouring nodes
        for neighbor in graph[current]:
            if neighbor not in visited:
                open_list.append((neighbor, path + [neighbor]))

    return None


# Run Greedy Best-First Search
start = "Arad"
goal = "Bucharest"

result = greedy_best_first_search(graph, heuristic, start, goal)

if result:
    print("Path found:", " -> ".join(result))
else:
    print("No path found.")


# lambda x: creates a small function that receives one entry from open_list.
# x[0] gets the city name, such as "Sibiu".
# heuristic[x[0]] gets that city's heuristic value, such as 253.
# sort() uses these values to arrange the entries in ascending order.

# def get_heuristic(x):
#     return heuristic[x[0]]

# open_list.sort(key=get_heuristic)