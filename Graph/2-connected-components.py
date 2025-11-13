class Solution:
    def findNumberOfComponent(self, V, edges):
        graph = self.createGraph(V, edges)
        visited = set()
        count = 0
        for i in range(V):
            if i not in visited:
                self.bfs(graph, i, visited)
                count = count + 1
        return count

    
    def bfs(self, graph, start, visited):
        queue = deque([start])
        visited.add(start)
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                visited.add(neighbor)
                queue.append(neighbor)
        
    def createGraph(self, V, edges):
        graph = defaultdict(list)
        for edge in edges:
            graph[edge[0]] = edge[1]
            graph[edge[1]] = edge[0]
        return graph
       
# Complexity Analysis
# Time Complexity: O(V+E),Each vertex is visited exactly once, and each edge is processed at most twice (once from each end).
# Space Complexity: O(V+E), To build Adjacency List.
