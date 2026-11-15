import heapq
# heapq is a built-in Python module that implements a priority queue using a min-heap.
# Define the graph with actual road distances
weighted_graph = {
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Zerind": {"Arad": 75, "Oradea": 71},
    "Sibiu": {"Arad": 140, "Oradea": 151, "Fagaras": 99, "Rimnicu Vilcea": 80},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Craiova": {"Drobeta": 120, "Rimnicu Vilcea": 146, "Pitesti": 138},
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "Rimnicu Vilcea": {"Sibiu": 80, "Craiova": 146, "Pitesti": 97},
    "Pitesti": {"Rimnicu Vilcea": 97, "Craiova": 138, "Bucharest": 101},
    "Bucharest": {"Fagaras": 211, "Pitesti": 101, "Giurgiu": 90, "Urziceni": 85},
    "Giurgiu": {"Bucharest": 90},
    "Urziceni": {"Bucharest": 85, "Hirsova": 98, "Vaslui": 142},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Eforie": {"Hirsova": 86},
    "Vaslui": {"Urziceni": 142, "Iasi": 92},
    "Iasi": {"Vaslui": 92, "Neamt": 87},
    "Neamt": {"Iasi": 87}
}

# Heuristic values: straight-line distances to Bucharest
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

# A* Search function
def a_star_search(graph, heuristic, start, goal):

    # Priority queue: (f_cost, g_cost, current_node, path)
    open_list = [(heuristic[start], 0, start, [start])]

    # Store the lowest known cost to reach each node
    g_costs = {start: 0}

    while open_list:

        # Get the node with the lowest f(n)
        f_cost, g_cost, current, path = heapq.heappop(open_list)

        # Ignore outdated entries with higher costs
        if g_cost > g_costs[current]:
            continue

        print("Visiting:", current, "| g =", g_cost,
              "| h =", heuristic[current], "| f =", f_cost)

        # Check whether the goal has been reached
        if current == goal:
            return path, g_cost

        # Explore neighbouring nodes
        for neighbor, distance in graph[current].items():

            new_g_cost = g_cost + distance

            # Update if a cheaper route is found
            if new_g_cost < g_costs.get(neighbor, float("inf")):

                g_costs[neighbor] = new_g_cost

                new_f_cost = new_g_cost + heuristic[neighbor]

                heapq.heappush(
                    open_list,
                    (new_f_cost, new_g_cost, neighbor, path + [neighbor])
                )

    return None, float("inf")


# Run A* Search
start = "Arad"
goal = "Bucharest"

result, total_cost = a_star_search(
    weighted_graph, heuristic, start, goal
)

if result:
    print("Shortest path:", " -> ".join(result))
    print("Total cost:", total_cost, "km")
else:
    print("No path found.")
