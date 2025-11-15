import heapq

def findShortestPath(graph, start, V):
    pq = []
    distance = [ float('inf') for _ in range(V)]
    distance[start] = 0
    heapq.heappush(pq, [0, start])

    while pq:
        wt, node = heapq.heappop(pq)
        for neighbor, wt in graph[node]:
            if distance[neighbor] > distance[node] + wt:
                distance[neighbor] = distance[node] + wt
                heapq.heappush(pq, [distance[neighbor], neighbor])
    return distance

def dijkstra_with_path(graph, start: int, V: int):
    """
    Dijkstra's algorithm that also returns the shortest path tree

    Returns:
        - distance: List of shortest distances
        - parent: Dict mapping each node to its predecessor in shortest path

    To reconstruct path from start to node X:
        path = []
        current = X
        while current != start:
            path.append(current)
            current = parent[current]
        path.append(start)
        path.reverse()
    """
    distance = [float('inf')] * V
    distance[start] = 0
    parent = {start: None}  # Track predecessors for path reconstruction

    pq = [(0, start)]
    visited = set()

    while pq:
        curr_dist, node = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)

        if node in graph:
            for neighbor, weight in graph[node]:
                new_dist = distance[node] + weight

                if new_dist < distance[neighbor]:
                    distance[neighbor] = new_dist
                    parent[neighbor] = node  # Track where we came from
                    heapq.heappush(pq, (new_dist, neighbor))

    return distance, parent


def main():
    V = 6
    graph ={
        0: [(1,1)],
        1: [(2,1)],
        2: [(3,5), (4,8)],
        3: [(4,2)],
        4: [(5,1)],
        5: []
    }
    #[0, 1, 2, 7, 9, 10]
    print(findShortestPath(graph, 0, V))
    print(dijkstra_with_path(graph, 0, V))

if __name__ == '__main__':
    main()
