from collections import deque #double ended queue

def bfs(graph, start):

    visited = set()
    queue = deque([start])

    visited.add(start)

    while queue:

        node = queue.popleft() # remove the elememt -> dequeue

        print(node, end=" ")

        for neighbor in graph[node]:

            if neighbor not in visited:

                visited.add(neighbor)
                queue.append(neighbor) # add at the end -> Enqueue
# adjacency list -> list of directly connected nodes.
graph = {
    0: [1, 4],
    1: [0, 4, 3, 2],
    2: [1, 3],
    3: [1, 2, 4],
    4: [0, 1, 3]
}

bfs(graph, 0)