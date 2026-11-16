import heapq

class Graph:

    def __init__(self):
        # Store the graph and heuristic values
        self.graph = {}
        self.heuristic = {}

    # Add a connection between two cities
    def add_edge(self, city1, city2, distance):
        if city1 not in self.graph:
            self.graph[city1] = {}

        if city2 not in self.graph:
            self.graph[city2] = {}

        self.graph[city1][city2] = distance
        self.graph[city2][city1] = distance

    # Set heuristic value for a city
    def add_heuristic(self, city, value):
        self.heuristic[city] = value

    # Task 1: Greedy Best-First Search
    def greedy_best_first_search(self, start, goal):

        open_list = [(self.heuristic[start], start, [start])]
        visited = set()

        while open_list:

            h_cost, current, path = heapq.heappop(open_list)

            if current in visited:
                continue

            print("Visiting:", current)

            if current == goal:
                return path

            visited.add(current)

            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    heapq.heappush(
                        open_list,
                        (self.heuristic[neighbor], neighbor, path + [neighbor])
                    )

        return None

    # Task 2: A* Search
    def a_star_search(self, start, goal):

        open_list = [(self.heuristic[start], 0, start, [start])]
        g_costs = {start: 0}

        while open_list:

            f_cost, g_cost, current, path = heapq.heappop(open_list)

            if g_cost > g_costs[current]:
                continue

            print("Visiting:", current, "| g =", g_cost,
                  "| h =", self.heuristic[current], "| f =", f_cost)

            if current == goal:
                return path, g_cost

            for neighbor, distance in self.graph[current].items():

                new_g_cost = g_cost + distance

                if new_g_cost < g_costs.get(neighbor, float("inf")):

                    g_costs[neighbor] = new_g_cost

                    new_f_cost = new_g_cost + self.heuristic[neighbor]

                    heapq.heappush(
                        open_list,
                        (new_f_cost, new_g_cost, neighbor, path + [neighbor])
                    )

        return None, float("inf")


# Create Graph object
g = Graph()

# Add cities and road distances
edges = [
    ("Arad", "Zerind", 75),
    ("Arad", "Sibiu", 140),
    ("Arad", "Timisoara", 118),
    ("Zerind", "Oradea", 71),
    ("Oradea", "Sibiu", 151),
    ("Sibiu", "Fagaras", 99),
    ("Sibiu", "Rimnicu Vilcea", 80),
    ("Timisoara", "Lugoj", 111),
    ("Lugoj", "Mehadia", 70),
    ("Mehadia", "Drobeta", 75),
    ("Drobeta", "Craiova", 120),
    ("Craiova", "Rimnicu Vilcea", 146),
    ("Craiova", "Pitesti", 138),
    ("Rimnicu Vilcea", "Pitesti", 97),
    ("Fagaras", "Bucharest", 211),
    ("Pitesti", "Bucharest", 101),
    ("Bucharest", "Giurgiu", 90),
    ("Bucharest", "Urziceni", 85),
    ("Urziceni", "Hirsova", 98),
    ("Hirsova", "Eforie", 86),
    ("Urziceni", "Vaslui", 142),
    ("Vaslui", "Iasi", 92),
    ("Iasi", "Neamt", 87)
]

for city1, city2, distance in edges:
    g.add_edge(city1, city2, distance)


# Heuristic values: straight-line distances to Bucharest
heuristics = {
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

for city, value in heuristics.items():
    g.add_heuristic(city, value)


# Task 1: Run Greedy Best-First Search
print("\n--- Task 1: Greedy Best-First Search ---")

greedy_path = g.greedy_best_first_search("Arad", "Bucharest")

if greedy_path:
    print("Path:", " -> ".join(greedy_path))
else:
    print("No path found.")


# Task 2: Run A* Search
print("\n--- Task 2: A* Search ---")

astar_path, total_cost = g.a_star_search("Arad", "Bucharest")

if astar_path:
    print("Path:", " -> ".join(astar_path))
    print("Total cost:", total_cost, "km")
else:
    print("No path found.")
