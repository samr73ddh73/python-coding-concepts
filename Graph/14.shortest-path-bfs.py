#for undirected unweighed graph
from collections import deque
def findShortestPath(graph, start, V, target):
    distance = [ float('inf') for _ in range(V)]
    distance[start] = 0
    queue = deque([(start, 0)])
    while(queue):
        node, level = queue.popleft()
        for neighbor in graph[node]:
            if distance[neighbor]== float('inf'):
                distance[neighbor] = level+1
                queue.append((neighbor, level+1))
            if neighbor == target:
                return distance[neighbor]
    return distance[target]


def main():
    V = 6
    graph ={
        0: [1],
        1: [2],
        2: [3, 4],
        3: [4],
        4: [5],
        5: []
    }

    print(findShortestPath(graph, 0, V, 5))

if __name__ == '__main__':
    main()
  
        


