from collections import deque
def detectCycleBfs(graph, n):
    queue = deque()
    visited = set()
    
    for i in range(n):
        if i not in visited:
            queue.append((i, -1))
            visited.add(i)
            while queue:
                node, parent = queue.popleft()
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        queue.append((neighbor, node))
                        visited.add(neighbor)
                    elif neighbor in visited and neighbor != parent:
                        return True
    return False        

