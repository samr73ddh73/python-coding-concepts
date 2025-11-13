from collections import deque
def detectCycleDfs(graph, n):
    queue = deque()
    visited = set()
    
    for i in range(n):
        if i not in visited:
            return dfs(graph, i, -1, visited)
    return False

def dfs(graph, start, parent, visited):
    visited.add(start)
    for neighbor in graph[start]:
        if neighbor not in visited:
            if dfs(graph, neighbor, start, visited):  # ✅ Check result
                return True  # ✅ Propagate cycle up
        elif neigbor != parent:
            return True
    return False

