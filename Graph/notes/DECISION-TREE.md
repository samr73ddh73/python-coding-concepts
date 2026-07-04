# 🌳 Graph Decision Tree

> Quick guide to choose the right graph algorithm for your problem

---

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

## Time Complexity Cheat Sheet

| Algorithm | Time | Space | Use When |
|-----------|------|-------|----------|
| BFS | O(V+E) | O(V) | Shortest path (unweighted) |
| DFS | O(V+E) | O(V) | Cycles, topological sort |
| Dijkstra | O((V+E)logV) | O(V) | Shortest path (weighted) |
| Kahn's Topo | O(V+E) | O(V) | Topological sort |
| DFS Topo | O(V+E) | O(V) | Topological sort |
| DSU Find | O(α(n)) | O(V) | Connectivity queries |
| DSU Union | O(α(n)) | O(V) | Dynamic connectivity |
| Connected Comp | O(V+E) | O(V) | Find components |

---

## Key Algorithm Choices

### 1. Shortest Path Decision

| Scenario | Algorithm | Time | Why |
|----------|-----------|------|-----|
| **Unweighted graph** | BFS | O(V+E) | All edges have weight 1 |
| **Weighted (non-negative)** | Dijkstra | O((V+E)logV) | Greedy picks minimum distance |
| **Weighted (with negatives)** | Bellman-Ford | O(V·E) | Can handle negative weights |
| **All pairs shortest** | Floyd-Warshall | O(V³) | Dynamic programming |

### 2. Cycle Detection Decision

| Graph Type | Algorithm | Key Idea |
|------------|-----------|----------|
| **Undirected** | DFS + parent check | Bidirectional edges—only one path back |
| **Directed** | DFS + pathVisited | Must distinguish cross edges from back edges |
| **Dynamic edges** | Union-Find (DSU) | Add edges incrementally, detect cycles |

**Critical:** For directed graphs, parent check alone is NOT enough! Need pathVisited set (nodes in current recursion stack).

### 3. Topological Sort Decision

| Approach | Algorithm | When to Use |
|----------|-----------|-------------|
| **Intuitive** | Kahn's Algorithm | Think in terms of dependencies |
| **DFS-based** | DFS post-order | Already using DFS for other checks |
| **Time** | Both O(V+E) | Pick based on comfort |

**Prerequisite:** Verify graph is a DAG first! No topological sort for cyclic graphs.

### 4. Connected Components Decision

| Approach | Time | Space | When |
|----------|------|-------|------|
| **DFS/BFS** | O(V+E) | O(V) | One-time queries |
| **Union-Find** | O(α(n)) | O(V) | Multiple/dynamic queries |

### 5. Matrix/Grid Problems

| Problem Type | Algorithm |
|---|---|
| **Multi-source (closest distance)** | Multi-source BFS (add all sources first) |
| **Flood fill / Connected region** | DFS or BFS (single source) |
| **Count regions** | DFS/BFS from each unvisited |
| **Path finding** | BFS (shortest), DFS (any path) |

---

## Common Pitfalls & Fixes

| Problem | ❌ Wrong | ✓ Correct |
|---------|---------|-----------|
| **BFS queue** | `list.pop(0)` O(n) | `deque.popleft()` O(1) |
| **Visited check** | Mark when dequeuing | Mark **when enqueueing** |
| **Multi-source BFS** | Add sources while processing | Add **ALL sources FIRST** |
| **Cycle (undirected)** | Forget parent check | `if neighbor != parent` |
| **Cycle (directed)** | Simple visited check | Use **pathVisited** (recursion stack) |
| **Topological sort** | Add nodes during processing | Add **AFTER processing all neighbors** |
| **Shortest path (weighted)** | Use BFS | Use **Dijkstra** |
| **Path reconstruction** | Store node IDs | Store **parent pointers** |
| **Grid boundaries** | Check visited first | Check **bounds first** |
| **Disconnected graph** | Process only one component | Loop **all unvisited nodes** |

---

## Interview Tips

1. **Always ask**: "Is the graph weighted?" → Changes algorithm
2. **DAG assumption**: "Is this acyclic?" → Allows topological sort
3. **Shortest path**: Unweighted=BFS, weighted=Dijkstra
4. **Cycles**: Directed=pathVisited, Undirected=parent check
5. **Optimization**: Use DSU for repeated connectivity checks
6. **Space**: Can modify matrix in-place instead of separate visited set
7. **Early termination**: Return immediately when target found
8. **Edge cases**: Empty graph, single node, disconnected components

---

*For detailed implementations, see the pattern files (BFS-pattern.md, DFS-pattern.md, etc.)*
