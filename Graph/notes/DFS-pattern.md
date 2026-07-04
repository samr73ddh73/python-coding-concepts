# DFS (Depth-First Search) Pattern

## Core Concept
- Explores graph **depth-first** (goes as far as possible before backtracking)
- Uses **STACK** (LIFO) — naturally via recursion or explicit stack
- Perfect for **topological sort**, **cycle detection**, **path finding**

## Time & Space Complexity
- **Time**: O(V + E) — visit each vertex once, process each edge once
- **Space**: O(V) — recursion stack / explicit stack + visited set

## When to Use DFS
✓ Topological sort (DAGs)  
✓ Cycle detection (directed & undirected)  
✓ Path finding (any path, not necessarily shortest)  
✓ Connected components  
✓ Backtracking problems  
✓ Strongly connected components (Tarjan's, Kosaraju's)  

Use **BFS** instead for: shortest path, level-order, minimum steps

---

## Code Pattern: Recursive DFS

```python
from typing import Dict, List, Set

def dfs_recursive(graph: Dict[int, List[int]], start: int, visited: Set[int] = None) -> List[int]:
    """DFS using recursion."""
    if visited is None:
        visited = set()
    
    visited.add(start)
    result = [start]
    
    for neighbor in graph.get(start, []):
        if neighbor not in visited:
            result.extend(dfs_recursive(graph, neighbor, visited))
    
    return result
```

**Characteristics:**
- Clean and intuitive
- Call stack provides implicit stack
- Risk: Stack overflow on very deep graphs (Python limit ≈ 3000)

---

## Code Pattern: Iterative DFS (Explicit Stack)

```python
from typing import Dict, List, Set

def dfs_iterative(graph: Dict[int, List[int]], start: int) -> List[int]:
    """DFS using explicit stack (avoids recursion limit)."""
    visited = set()
    stack = [start]
    result = []
    
    while stack:
        node = stack.pop()  # LIFO - stack behavior
        
        if node not in visited:
            visited.add(node)
            result.append(node)
            
            # Add neighbors to stack (reverse order for left-to-right visit)
            for neighbor in reversed(graph.get(node, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return result
```

**Key Points:**
- Can handle deeper graphs (no recursion limit)
- Reverse neighbor order to visit in original order
- Mark visited when **popping** (not when pushing)

---

## Code Pattern: DFS with 3-State Coloring (Cycle Detection)

```python
def has_cycle_directed(graph: Dict[int, List[int]]) -> bool:
    """Detect cycle in directed graph using 3-state coloring."""
    # States: 0 = white (unvisited), 1 = gray (in-progress), 2 = black (done)
    color = {node: 0 for node in graph}
    
    def dfs(node):
        if color[node] == 1:  # Back edge - CYCLE FOUND
            return True
        if color[node] == 2:  # Already fully processed
            return False
        
        color[node] = 1  # Mark as in-progress (gray)
        
        for neighbor in graph.get(node, []):
            if dfs(neighbor):
                return True
        
        color[node] = 2  # Mark as done (black)
        return False
    
    # Check all nodes (handles disconnected components)
    for node in graph:
        if color[node] == 0:
            if dfs(node):
                return True
    
    return False
```

**3-Color Scheme:**
- **White (0)**: Unvisited
- **Gray (1)**: Currently being processed (in call stack)
- **Black (2)**: Fully processed
- **Back edge** (gray → gray) = cycle exists

---

## Code Pattern: Topological Sort (Kahn's via DFS)

```python
def topological_sort_dfs(graph: Dict[int, List[int]]) -> List[int]:
    """Topological sort for DAG using DFS."""
    visited = set()
    stack = []  # Will store nodes in reverse topological order
    
    def dfs(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
        stack.append(node)  # Add after processing all neighbors
    
    # Process all nodes
    for node in graph:
        if node not in visited:
            dfs(node)
    
    return stack[::-1]  # Reverse to get topological order
```

**Key Insight:**
- Post-order DFS: add to stack **AFTER** processing neighbors
- Reverse the stack to get topological order
- Only works for DAGs (directed acyclic graphs)

---

## Code Pattern: Find All Paths (Backtracking with DFS)

```python
def find_all_paths(graph: Dict[int, List[int]], start: int, end: int) -> List[List[int]]:
    """Find ALL paths from start to end."""
    result = []
    path = [start]
    visited = {start}
    
    def dfs(node):
        if node == end:
            result.append(path[:])  # Make a copy
            return
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)
                dfs(neighbor)
                path.pop()  # Backtrack
                visited.remove(neighbor)
    
    dfs(start)
    return result
```

**Backtracking Pattern:**
- Maintain current path and visited set
- Add node → explore → remove node (backtrack)
- Copy path when reaching destination

---

## Code Pattern: DFS with Parent Tracking (Cycle in Undirected)

```python
def has_cycle_undirected(graph: Dict[int, List[int]]) -> bool:
    """Detect cycle in undirected graph."""
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:  # Back edge (not to parent)
                return True
        
        return False
    
    # Check all components
    for node in graph:
        if node not in visited:
            if dfs(node, -1):
                return True
    
    return False
```

**Difference from Directed:**
- Track parent to distinguish back edge from forward edge
- Neighbor != parent means back edge (cycle)

---

## Code Pattern: Connected Components

```python
def find_components(graph: Dict[int, List[int]]) -> List[List[int]]:
    """Find all connected components."""
    visited = set()
    components = []
    
    def dfs(node, component):
        visited.add(node)
        component.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, component)
    
    for node in graph:
        if node not in visited:
            component = []
            dfs(node, component)
            components.append(component)
    
    return components
```

**Use Cases:**
- Finding isolated subgraphs
- Network connectivity analysis
- Graph segmentation

---

## Code Pattern: DFS on Matrix/Grid

```python
def dfs_matrix(matrix: List[List[int]], row: int, col: int, visited: Set = None) -> List[tuple]:
    """DFS on 2D grid."""
    if visited is None:
        visited = set()
    
    rows, cols = len(matrix), len(matrix[0])
    
    # Boundary & visited check
    if not (0 <= row < rows and 0 <= col < cols) or (row, col) in visited:
        return []
    
    if matrix[row][col] == 0:  # Obstacle or water
        return []
    
    visited.add((row, col))
    result = [(row, col)]
    
    # 4-directional movement
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        result.extend(dfs_matrix(matrix, row + dr, col + dc, visited))
    
    return result
```

**Grid-specific:**
- Check boundaries before recursing
- Check cell value (land/water, etc.)
- Maintain visited set across recursive calls

---

## Recursive vs Iterative DFS

| Aspect | Recursive | Iterative |
|--------|-----------|-----------|
| **Code Length** | Shorter, cleaner | More verbose |
| **Stack Usage** | Call stack | Explicit stack |
| **Depth Limit** | Python ≈ 3000 | Limited by memory |
| **Performance** | Slightly faster | Slightly slower |
| **Intuitive** | Yes, for most | Less intuitive |
| **Best For** | Normal graphs | Very deep graphs |

---

## Common Pitfalls ⚠️

| Pitfall | Problem | Solution |
|---------|---------|----------|
| **Cycle Detection (Directed)** | Forget parent tracking | Use 3-color scheme (white/gray/black) |
| **Cycle Detection (Undirected)** | Count as cycle going back to parent | Track parent: `if neighbor != parent` |
| **Topological Sort** | Add nodes in wrong order | Add **after** processing neighbors (post-order) |
| **All Paths** | Forget to backtrack | Use `path.pop()` and `visited.remove()` |
| **Stack Overflow** | Recursive DFS on deep graph | Use iterative version with explicit stack |
| **Disconnected Graph** | Only process one component | Loop through all nodes, DFS each unvisited |

---

## Edge Cases to Handle

```python
# Empty graph
if not graph:
    return []

# Single node
if len(graph) == 1:
    return list(graph.keys())

# Disconnected components
for node in graph:
    if node not in visited:
        dfs(node)

# Self-loops
handled by visited set

# DAG vs Cyclic
cycle detection required before topological sort
```

---

## Complexity Summary

| Variant | Time | Space | Use Case |
|---------|------|-------|----------|
| Basic DFS | O(V+E) | O(V) recursion | Traversal |
| Cycle Detect | O(V+E) | O(V) | Check cycles |
| Topological Sort | O(V+E) | O(V) | DAG ordering |
| All Paths | O(V!) worst | O(V) | Path enumeration |
| Components | O(V+E) | O(V) | Connectivity |
| Matrix DFS | O(rows×cols) | O(rows×cols) | Grid problems |

---

## Interview Tips 💡

1. **Ask about cycles**: "Is this DAG?" → Changes the algorithm choice
2. **Recursive limit**: For deep graphs, mention iterative version
3. **Backtracking**: Explicitly show add/explore/remove pattern
4. **Cycle detection**: Different for directed (3-color) vs undirected (parent check)
5. **Topological sort**: Always verify it's a DAG first
6. **Post-order traversal**: Perfect for building results after exploring subtrees
7. **Early termination**: Return immediately if condition found (especially in cycle detection)
