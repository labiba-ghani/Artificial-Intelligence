
# Task 3: 8-Puzzle Problem using A* Search

import heapq

# Define initial and goal states
initial_state = (1, 2, 3,
                 4, 0, 6,
                 7, 5, 8)

goal_state = (1, 2, 3,
              4, 5, 6,
              7, 8, 0)


# Calculate the number of misplaced tiles
def heuristic(state, goal):
    count = 0

    for i in range(9):
        if state[i] != 0 and state[i] != goal[i]:
            count += 1

    return count


# Generate possible next states
def get_neighbors(state):

    neighbors = []
    zero_index = state.index(0)

    row = zero_index // 3
    col = zero_index % 3

    # Possible movements: up, down, left, right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in moves:

        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < 3 and 0 <= new_col < 3:

            new_index = new_row * 3 + new_col

            new_state = list(state)

            # Swap the empty space with a neighbouring tile
            new_state[zero_index], new_state[new_index] = (
                new_state[new_index], new_state[zero_index]
            )

            neighbors.append(tuple(new_state))

    return neighbors


# A* Search algorithm
def a_star_puzzle(start, goal):

    # Priority queue: (f_cost, g_cost, state, path)
    open_list = [(heuristic(start, goal), 0, start, [start])]

    g_costs = {start: 0}

    while open_list:

        f_cost, g_cost, current, path = heapq.heappop(open_list)

        # Ignore outdated entries
        if g_cost > g_costs[current]:
            continue

        # Check if the goal state is reached
        if current == goal:
            return path

        # Explore possible next states
        for neighbor in get_neighbors(current):

            new_g_cost = g_cost + 1

            if new_g_cost < g_costs.get(neighbor, float("inf")):

                g_costs[neighbor] = new_g_cost

                new_f_cost = new_g_cost + heuristic(neighbor, goal)

                heapq.heappush(
                    open_list,
                    (new_f_cost, new_g_cost, neighbor, path + [neighbor])
                )

    return None


# Display the puzzle in a 3x3 grid
def print_puzzle(state):

    for i in range(0, 9, 3):
        print(state[i:i + 3])

    print()


# Run the A* algorithm
solution = a_star_puzzle(initial_state, goal_state)

if solution:

    print("Solution found!")
    print("Total moves:", len(solution) - 1)

    for step, state in enumerate(solution):

        print("Step:", step)
        print_puzzle(state)

else:
    print("No solution found.")
