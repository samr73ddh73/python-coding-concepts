# BFS (Breadth-First Search) Pattern

## Core Concept
- Explores graph **level by level** (nearest neighbors first)
- Uses **QUEUE (FIFO)** data structure
- Guarantees **shortest path** in unweighted graphs

## Time & Space Complexity
- **Time**: O(V + E) — visit each vertex once, process each edge once
- **Space**: O(V) — queue + visited set

## When to Use BFS
✓ Shortest path in unweighted graphs  
✓ Level-order traversal  
✓ Finding connected components  
✓ Minimum steps problems  
✓ Multi-source shortest path  

Use **DFS** instead for: topological sort, cycle detection, backtracking

---

## Code Pattern: Basic BFS

```python
from collections import deque
from typing import Dict, List

def bfs_basic(graph: Dict[int, List[int]], start: int) -> List[int]:
    """Return nodes in BFS visit order."""
    if not graph or start not in graph:
        return []
    
    visited = set()
    queue = deque([start])
    visited.add(start)
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        # Process all neighbors
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)  # Mark BEFORE adding to queue!
                queue.append(neighbor)
    
    return result
```

**Key Points:**
- Mark visited **BEFORE** adding to queue (prevents duplicates)
- Use `deque` for O(1) popleft() — never use `list.pop(0)` which is O(n)!
- Use `set` for visited (O(1) lookup) — never use `list` (O(n) lookup)

---

## Code Pattern: BFS with Distance Tracking

```python
def bfs_with_distance(graph: Dict[int, List[int]], start: int) -> Dict[int, int]:
    """Track distance/level of each vertex from start."""
    if not graph or start not in graph:
        return {}
    
    distances = {start: 0}
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        current_dist = distances[node]
        
        for neighbor in graph[node]:
            if neighbor not in distances:
                distances[neighbor] = current_dist + 1
                queue.append(neighbor)
    
    return distances
```

**Use Cases:**
- Shortest path problems
- Minimum steps to reach target
- Distance matrix computation

---

## Code Pattern: Shortest Path with Parent Tracking

```python
def bfs_shortest_path(graph: Dict[int, List[int]], start: int, target: int) -> List[int]:
    """Find shortest path from start to target."""
    if start == target:
        return [start]
    
    visited = {start}
    queue = deque([start])
    parent = {start: None}
    
    while queue:
        node = queue.popleft()
        
        if node == target:
            # Reconstruct path
            path = []
            current = target
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)
    
    return []  # No path found
```

**Reconstruction Logic:**
- Store parent of each node
- When target found, backtrack: `child → parent → ... → start`
- Reverse the path to get start → target

---

## Code Pattern: Multi-Source BFS

```python
def bfs_multi_source(graph: Dict[int, List[int]], sources: List[int]) -> Dict[int, int]:
    """Start from multiple vertices simultaneously."""
    distances = {}
    queue = deque()
    
    # Initialize: add ALL sources to queue first
    for source in sources:
        if source in graph:
            distances[source] = 0
            queue.append(source)
    
    while queue:
        node = queue.popleft()
        current_dist = distances[node]
        
        for neighbor in graph[node]:
            if neighbor not in distances:
                distances[neighbor] = current_dist + 1
                queue.append(neighbor)
    
    return distances
```

**Critical Point:**
- Add **ALL sources to queue FIRST** before starting BFS
- This ensures all sources have distance 0
- Used in: Rotting Oranges, Walls & Gates, etc.

---

## Code Pattern: Matrix/Grid BFS (4-Directional)

```python
from typing import List, Tuple

def bfs_matrix(matrix: List[List[int]], start_row: int, start_col: int) -> List[Tuple]:
    """BFS on 2D grid with 4-directional movement."""
    if not matrix or not matrix[0]:
        return []
    
    rows, cols = len(matrix), len(matrix[0])
    
    visited = set()
    queue = deque([(start_row, start_col)])
    visited.add((start_row, start_col))
    result = []
    
    # 4-directional: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # For 8-directional: add [(-1,-1), (-1,1), (1,-1), (1,1)]
    
    while queue:
        row, col = queue.popleft()
        result.append((row, col))
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            
            # Check boundaries & visited
            if (0 <= new_row < rows and
                0 <= new_col < cols and
                (new_row, new_col) not in visited and
                matrix[new_row][new_col] == 1):
                
                visited.add((new_row, new_col))
                queue.append((new_row, new_col))
    
    return result
```

**Grid Template:**
- Directions tuple for reuse
- Always check boundaries first
- Common condition: cell value == 1 (adjust as needed)

---

## Code Pattern: Level-Order Traversal

```python
def bfs_by_levels(graph: Dict[int, List[int]], start: int) -> List[List[int]]:
    """Return nodes grouped by level."""
    if not graph or start not in graph:
        return []
    
    levels = []
    queue = deque([start])
    visited = {start}
    
    while queue:
        level_size = len(queue)  # Capture current level size
        current_level = []
        
        # Process exactly level_size nodes (one level)
        for _ in range(level_size):
            node = queue.popleft()
            current_level.append(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        levels.append(current_level)
    
    return levels
```

**Key Trick:**
- Save `level_size = len(queue)` at start of each iteration
- Process exactly `level_size` nodes
- This groups nodes by their distance from start

---

## Common Pitfalls ⚠️

| Pitfall | Wrong | Right |
|---------|-------|-------|
| **Queue Implementation** | `queue.pop(0)` → O(n) | `deque.popleft()` → O(1) |
| **Visited Tracking** | Mark when popping | Mark **when enqueueing** |
| **Visited Data Structure** | `if node in list_visited` → O(n) | `if node in set_visited` → O(1) |
| **Multi-source** | Add sources while processing | Add **ALL sources first** |
| **Grid Boundaries** | Check visited after bounds | Check **bounds first** |
| **Distance Type** | Store as instance variable | Store in **dict/visited** |

---

## Edge Cases to Handle

```python
# Empty/Invalid
if not graph or start not in graph:
    return []

# Single node
if start == target:
    return [start]

# Disconnected graph (use all components)
for vertex in graph:
    if vertex not in visited:
        bfs_from(vertex)

# Self-loops & cycles
# Handled automatically by visited set

# Out of bounds (grid)
if not (0 <= new_row < rows and 0 <= new_col < cols):
    continue
```

---

## Complexity Summary

| Variant | Time | Space | Use Case |
|---------|------|-------|----------|
| Basic BFS | O(V+E) | O(V) | Traversal |
| With Distance | O(V+E) | O(V) | Shortest path |
| Shortest Path | O(V+E) | O(V) | Find actual path |
| Multi-Source | O(V+E) | O(V) | Rotting oranges |
| Matrix (4-dir) | O(rows×cols) | O(rows×cols) | Grid problems |
| Level-Order | O(V+E) | O(width) | Tree/Graph levels |

---

## Interview Tips 💡

1. **Always ask**: "Is the graph weighted?" → If yes, use Dijkstra, not BFS
2. **Early termination**: Return immediately when target found (don't traverse entire graph)
3. **Multi-source**: Remember to add ALL sources before starting BFS
4. **Grid problems**: Predefine direction vectors for cleaner code
5. **Space optimization**: Can sometimes use visited within the matrix itself instead of separate set
