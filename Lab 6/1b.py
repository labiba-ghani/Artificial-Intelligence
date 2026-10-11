
def dfs_recursive(graph, node, visited):
    visited.add(node)
    print(node, end=" ")

    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)

# If the neighbour has not been visited, call the same function again using that neighbour.
graph = {
    1: [2, 7, 8],
    2: [3, 6],
    3: [4, 5],
    4: [],
    5: [],
    6: [],
    7: [],
    8: [9, 12],
    9: [10, 11],
    10: [],
    11: [],
    12: []
}

visited = set()
dfs_recursive(graph, 1, visited)

# Let's understand the important moment when DFS reaches node 4.
# 1. dfs(1) calls dfs(2).
# 2. dfs(2) calls dfs(3).
# 3. dfs(3) calls dfs(4).
# 4. dfs(4) finds no neighbours, so it returns.
# 5. Execution resumes inside dfs(3), which then calls dfs(5).
# 6. After node 5 finishes, dfs(3) returns to dfs(2).
# 7. dfs(2) continues and visits node 6.