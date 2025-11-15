# - basically for directed acyclic graphs, we want to find the order such that if 
# u, v is an edge, u always comes before v

# - simple dfs:

# you have to keep going and jab backtrack kr rhe hai tab stack me add kr do, because backtrack time, vaha vala dfs khatam, so order me hoga
from collections import deque

def topoSort( graph, V):
    queue = deque()
    visited = set()
    stack = []
    for i in range(V):
        if i not in visited:
            dfs(graph, i, visited, stack)
    return stack[::-1]

def dfs(graph, start, visited, stack):
    visited.add(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited, stack)
    stack.append(start)

def main():
    V = 6
    graph ={
        0: [],
        1: [],
        2: [3],
        3: [1],
        4: [0,1],
        5: [0,2]
    }

    print(topoSort(graph, V))

if __name__ == '__main__':
    main()