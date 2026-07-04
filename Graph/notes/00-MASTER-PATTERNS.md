# Graph Patterns Master Guide — Quick Revision

## Quick Decision Tree

```
Problem Analysis:
├─ Shortest path?
│  ├─ Unweighted → BFS O(V+E)
│  └─ Weighted → Dijkstra O((V+E)logV)
│
├─ Cycle detection?
│  ├─ Undirected → DFS parent check OR BFS parent check (parent check is enough)
│  └─ Directed → DFS with pathVisited (REMEMBER THIS)
│
├─ Topological sort?
│  ├─ Verify DAG first!
│  └─ Use Kahn's (BFS) OR DFS post-order
│
├─ Connected components?
│  ├─ DFS/BFS from unvisited
│  └─ OR Union-Find
│
├─ Matrix/Grid problem?
│  ├─ Multi-source BFS (Rotten Oranges)
│  └─ OR DFS for flood fill
│
└─ General traversal?
   └─ DFS for depth, BFS for breadth
```

---

## 1. CYCLE DETECTION — Key Insight

### Why Parent Check for Undirected?
```
Graph: 0 — 1 — 2
       |_______|

Undirected edges are bidirectional: 0↔1 means both directions!
When visiting 1 from 0, see 0 is visited.
But that's NOT a cycle — it's the edge we came from!

✓ Parent check prevents false positives:
  - if neighbor is visited AND is parent → skip
  - if neighbor is visited AND NOT parent → CYCLE!
```

### Undirected: DFS with Parent Check
```python
def has_cycle_undirected(graph, n):
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:  # Back edge to non-parent = cycle
                return True
        return False
    
    for i in range(n):
        if i not in visited:
            if dfs(i, -1):
                return True
    return False
```

### Directed: DFS with pathVisited (NOT 3-Color) — Parent Check Fails!

**Why parent check fails for directed graphs:**
```
Cross Edge Example (NO CYCLE):     Cycle Example (HAS CYCLE):
    0 → 1                               0 → 1 → 2
    ↓   ↓                               ↑   |
    2 → 3                               └───┘

With parent check only:
  When we reach 3 from 0→2→3:
    "3 already visited? Check if parent=2"
    "Parent is 2, but 3 was also visited from 1"
    "NOT parent? → FALSE CYCLE!" ❌ WRONG!

The problem: Can't distinguish between:
  - Cross edge: 0→1→3 and 0→2→3 (both lead to same node)
  - Back edge: 1→2→1 (loop in current path)
```

**Solution: Use pathVisited (current DFS path)**
```python
def dfsHasCycle(graph, start, visited, pathVisited):
    visited.add(start)
    pathVisited.add(start)  # Add to CURRENT path only

    for neighbor in graph[start]:
        # Case 1: Back edge! (neighbor in CURRENT path = cycle)
        if neighbor in pathVisited:
            return True  # CYCLE DETECTED! ✅

        # Case 2: Unvisited - explore it
        if neighbor not in visited:
            if dfsHasCycle(graph, neighbor, visited, pathVisited):
                return True

        # Case 3: visited but NOT in pathVisited
        # This is a cross/forward edge - SAFE ✅

    pathVisited.remove(start)  # Backtrack - remove from current path
    return False
```

**Key Insight: pathVisited = nodes in current recursion stack**
- If neighbor in pathVisited → back edge (loop) → CYCLE!
- If neighbor in visited but NOT pathVisited → cross edge (safe)
- After returning, remove from pathVisited so other branches don't skip this node

**Why it works:**
```
No Cycle:
DFS(0, pathVisited={0}):
  DFS(1, pathVisited={0,1}):
    DFS(3, pathVisited={0,1,3}):
      Return, remove 3: pathVisited={0,1}
    Return, remove 1: pathVisited={0}
  DFS(2, pathVisited={0,2}):
    See 3: in visited? Yes, in pathVisited={0,2}? NO → cross edge ✅

Cycle:
DFS(0, pathVisited={0}):
  DFS(1, pathVisited={0,1}):
    DFS(2, pathVisited={0,1,2}):
      See 1: in pathVisited={0,1,2}? YES → back edge → CYCLE! ✅
```

**Key Difference:**
- **Undirected:** Bidirectional edges → parent check enough (only one path back)
- **Directed:** One-way edges → pathVisited needed (distinguish cross vs back edges)

---

## 2. TOPOLOGICAL SORT — For DAGs Only

### When to Use
```
✓ Task scheduling (prerequisites)
✓ Dependency resolution
✓ Build systems
✓ Compile order

⚠️ ONLY works for DAGs (Directed Acyclic Graphs)!
   Always check for cycles first!
```

### Time & Space Complexity
```
BOTH algorithms (Kahn's and DFS):

TIME: O(V + E)
  - Visit each vertex exactly once: O(V)
  - Process each edge exactly once: O(E)
  - Total: O(V + E)

SPACE: O(V)
  - Queue/Stack: O(V) for nodes
  - In-degree array (Kahn's): O(V)
  - Visited set (DFS): O(V)
  - Recursion stack (DFS): O(V) worst case
```

### Kahn's Algorithm (BFS-based)
```python
def topological_sort_kahns(graph, n):
    # Count in-degrees: O(V + E)
    in_degree = [0] * n
    adj = defaultdict(list)
    
    for u in graph:
        for v in graph[u]:
            adj[u].append(v)
            in_degree[v] += 1
    
    # Queue of nodes with in-degree 0
    queue = deque([i for i in range(n) if in_degree[i] == 0])
    result = []
    
    while queue:  # Each node processed once: O(V)
        node = queue.popleft()
        result.append(node)
        
        for neighbor in adj[node]:  # Each edge processed once: O(E)
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return result if len(result) == n else []  # Empty = cycle
```

**How it works:**
1. Nodes with in-degree 0 have no dependencies
2. Remove them and decrease in-degree of neighbors
3. When a neighbor's in-degree becomes 0, it has no more dependencies
4. If can't process all nodes → cycle exists

### DFS Post-order
```python
def topological_sort_dfs(graph, n):
    visited = set()
    stack = []
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph.get(node, []):  # Each edge once: O(E)
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)  # Add AFTER processing neighbors (post-order)
    
    for i in range(n):  # Each node once: O(V)
        if i not in visited:
            dfs(i)
    
    return stack[::-1]  # Reverse for topological order
```

**Key Insight:** 
- Post-order DFS adds nodes when backtracking
- Leaves get added first, root last
- Reversing gives topological order (dependencies first)

**Why post-order works:**
```
    0 → 1 → 2
    └→ 3

DFS(0):
  DFS(1):
    DFS(2): add 2 to stack
  add 1 to stack
  DFS(3): add 3 to stack
add 0 to stack

Stack: [2, 1, 3, 0]
Reverse: [0, 3, 1, 2]

Check: 0 before 1✓, 0 before 3✓, 1 before 2✓
```

### Which Algorithm to Use?

| Aspect | Kahn's | DFS |
|--------|--------|-----|
| **Approach** | BFS (level by level) | DFS (depth first) |
| **Detects cycles** | Naturally (count != n) | Can add check |
| **Intuitive** | More intuitive (dependencies) | Less intuitive |
| **Performance** | O(V+E) same | O(V+E) same |
| **Space** | Queue | Recursion stack |
| **Best for** | Most interviews | Already in recursion |

---

## 3. SHORTEST PATH — Choose by Weight

### Unweighted Graph → BFS O(V+E)
```python
def shortest_path_bfs(graph, start, target):
    if start == target:
        return [start]
    
    visited = {start}
    queue = deque([start])
    parent = {start: None}
    
    while queue:
        node = queue.popleft()
        
        if node == target:
            # Reconstruct: backtrack through parents
            path = []
            while node:
                path.append(node)
                node = parent[node]
            return path[::-1]
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)
    
    return []
```

### Weighted Graph → Dijkstra O((V+E)logV)
```python
import heapq

def dijkstra(graph, start, target):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parent = {start: None}
    
    pq = [(0, start)]  # (distance, node)
    
    while pq:
        curr_dist, node = heapq.heappop(pq)
        
        if curr_dist > distances[node]:  # Already found shorter path
            continue
        
        for neighbor, weight in graph[node]:
            new_dist = curr_dist + weight
            
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                parent[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))
    
    # Reconstruct path
    path = []
    node = target
    while node:
        path.append(node)
        node = parent.get(node)
    return path[::-1] if path[0] == start else []
```

---

## 4. MULTI-SOURCE PROBLEMS

### Rotten Oranges Pattern
```python
def orangesRotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    
    # Step 1: Add ALL rotten oranges to queue
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 2:
                queue.append((i, j, 0))  # row, col, time
            elif grid[i][j] == 1:
                fresh += 1
    
    # Step 2: BFS from all sources simultaneously
    directions = [(0,1), (0,-1), (1,0), (-1,0)]
    while queue and fresh > 0:
        r, c, time = queue.popleft()
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 2
                fresh -= 1
                queue.append((nr, nc, time + 1))
    
    return -1 if fresh > 0 else time if queue or fresh == 0 else 0
```

**Key Insight:** Add ALL sources first, then BFS from all simultaneously

---

## 5. UNION-FIND (DSU) — For Cycle Detection & Connectivity

### When to Use DSU Over DFS/BFS
```
✓ Multiple connectivity queries
✓ Dynamic connectivity (add edges gradually)
✓ Redundant connection detection
✓ Friend circles

vs.

BFS/DFS: One-time connectivity check
DSU: Repeated queries or dynamic edges
```

### Implementation
```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):  # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):  # Union by rank
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False  # Already connected
        
        # Attach smaller to larger
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        return True

# Cycle detection: if union returns False, edge creates cycle
dsu = DSU(n)
for u, v in edges:
    if not dsu.union(u, v):
        return True  # Cycle found
```

---

## 6. MATRIX/GRID PATTERNS

### Key Template
```python
def grid_problem(matrix):
    rows, cols = len(matrix), len(matrix[0])
    visited = set()
    
    # Direction vectors for 4-connected grid
    directions = [(-1,0), (1,0), (0,-1), (0,1)]
    # For 8-connected: add [(-1,-1), (-1,1), (1,-1), (1,1)]
    
    def bfs(start_r, start_c):
        queue = deque([(start_r, start_c)])
        visited.add((start_r, start_c))
        
        while queue:
            r, c = queue.popleft()
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 
                    0 <= nc < cols and 
                    (nr, nc) not in visited and
                    matrix[nr][nc] == 1):  # Adjust condition as needed
                    
                    visited.add((nr, nc))
                    queue.append((nr, nc))
    
    # Handle multiple starting points or connected components
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == <initial_state> and (i, j) not in visited:
                bfs(i, j)
```

---

## 7. CONNECTED COMPONENTS

```python
def find_components(graph, n):
    visited = set()
    components = []
    
    def dfs(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, component)
    
    for i in range(n):
        if i not in visited:
            component = []
            dfs(i, component)
            components.append(component)
    
    return components

# OR using DSU
dsu = DSU(n)
for u, v in edges:
    dsu.union(u, v)
components = len(set(dsu.find(i) for i in range(n)))
```

---

## COMMON PITFALLS & FIXES

| Problem | ❌ Wrong | ✓ Correct |
|---------|---------|-----------|
| **BFS queue** | `list.pop(0)` O(n) | `deque.popleft()` O(1) |
| **Visited check** | Mark when dequeuing | Mark **when enqueueing** |
| **Multi-source BFS** | Add sources while processing | Add **ALL sources FIRST** |
| **Cycle (undirected)** | Forget parent check | `if neighbor != parent` |
| **Cycle (directed)** | Simple visited check | Use **3-color scheme** |
| **Topological sort** | Add nodes during processing | Add **AFTER processing all neighbors** |
| **Shortest path (weighted)** | Use BFS | Use **Dijkstra** |
| **Path reconstruction** | Store node IDs | Store **parent pointers** |
| **Grid boundaries** | Check visited first | Check **bounds first** |
| **Disconnected graph** | Process only one component | Loop **all unvisited nodes** |

---

## REDUNDANCY ANALYSIS — Your Existing Files

### ✅ Keep Separate (Good Organization)
- `BFS-pattern.md` — Detailed BFS with 6 code patterns
- `DFS-pattern.md` — Detailed DFS with 8 code patterns
- `0-DSU-notes.md` — Specialized DSU guide

### ⚠️ Redundant/Incomplete
- `patterns.md` — Too brief, Hindi notes, unclear
  - Recommendation: **DELETE**, use this master file instead
- `20-when-to-use-bfs-dfs.md` — Incomplete (1 line)
  - Recommendation: **DELETE**, covered in this file's decision tree

---

## TIME COMPLEXITY CHEAT SHEET

| Algorithm | Time | Space | Use When |
|-----------|------|-------|----------|
| BFS | O(V+E) | O(V) | Shortest path (unweighted) |
| DFS | O(V+E) | O(V) | Cycles, topological sort |
| Dijkstra | O((V+E)logV) | O(V) | Shortest path (weighted) |
| Kahn's Topo | O(V+E) | O(V) | Topological sort |
| DFS Topo | O(V+E) | O(V) | Topological sort |
| DSU Find | O(α(n)) | O(V) | Connectivity queries |
| DSU Union | O(α(n)) | O(V) | Dynamic connectivity |
| Connected Comp (DFS) | O(V+E) | O(V) | Find components |

---

## INTERVIEW QUICK TIPS

1. **Always ask**: "Is the graph weighted?" → Changes algorithm
2. **DAG assumption**: "Is this acyclic?" → Allows topological sort
3. **Shortest path**: Unweighted=BFS, weighted=Dijkstra
4. **Cycles**: Directed=3-color, Undirected=parent check
5. **Optimization**: Use DSU for repeated connectivity checks
6. **Space**: Can modify matrix in-place instead of separate visited set
7. **Early termination**: Return immediately when target found
8. **Edge cases**: Empty graph, single node, disconnected components
