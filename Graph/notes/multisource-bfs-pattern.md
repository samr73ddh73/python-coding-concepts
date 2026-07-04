# Multi-Source BFS Pattern

## Problem: As Far from Land as Possible
**LeetCode 1162** | [Problem Link](https://leetcode.com/problems/as-far-from-land-as-possible/)

Given an `n x n` grid containing `1`s (land) and `0`s (water), return the maximum distance from any water cell to the nearest land cell. If there is no land or no water, return `-1`.

Distance is measured by the **shortest path** (BFS).

---

## Solution

```python
class Solution:
    def maxDistance(self, grid: List[List[int]]) -> int:
        if not grid and not grid[0]:
            return -1
        
        waterCount = 0
        queue = deque([])
        visited = set()
        row, col = len(grid), len(grid[0])
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
        
        # Start from ALL land cells simultaneously
        for i in range(row):
            for j in range(col):
                if grid[i][j] == 1:
                    queue.append((i, j, 0))
                    visited.add((i, j))
                else:
                    waterCount += 1
        
        # Edge case: all land or all water
        if waterCount == 0 or len(queue) == 0:
            return -1
        
        maxDist = float('-inf')
        
        # Multi-source BFS: expand from all lands simultaneously
        while queue:
            r, c, dist = queue.popleft()
            
            for dx, dy in directions:
                x, y = r + dx, c + dy
                if 0 <= x < row and 0 <= y < col and (x, y) not in visited:
                    if grid[x][y] == 0:  # Found water
                        maxDist = max(maxDist, dist + 1)
                        queue.append((x, y, dist + 1))
                        visited.add((x, y))
        
        return maxDist
```

**Time Complexity**: O(n²) — each cell visited once  
**Space Complexity**: O(n²) — queue + visited set

---

## How It Works (Step-by-Step)

### Step 1: Initialize from ALL Lands
```python
for i in range(row):
    for j in range(col):
        if grid[i][j] == 1:
            queue.append((i, j, 0))  # Add all lands with distance 0
            visited.add((i, j))
```
- Instead of starting from one cell, we start from **all land cells simultaneously**
- Each land has distance `0` to itself
- This is the key difference from single-source BFS

### Step 2: Expand Outward
```python
while queue:
    r, c, dist = queue.popleft()
    
    for dx, dy in directions:
        x, y = r + dx, c + dy
        if 0 <= x < row and 0 <= y < col and (x, y) not in visited:
            if grid[x][y] == 0:  # Only process water cells
                maxDist = max(maxDist, dist + 1)
                queue.append((x, y, dist + 1))
```
- **Multi-source expansion**: All lands expand outward simultaneously (like a wave)
- When we reach a water cell, its distance = distance from nearest land
- We track the maximum distance found

### Step 3: Last Water Cell = Furthest
```
Initial:           After dist 1:      After dist 2:      After dist 3:
1 0 0 0            1 1 0 0            1 1 1 0            1 1 1 1
0 0 0 1    ───→    1 1 0 1    ───→    1 1 1 1    ───→    1 1 1 1
0 0 0 0            0 1 0 1            0 1 1 1            1 1 1 1
1 0 0 0            1 1 0 0            1 1 1 0            1 1 1 1
                                                           ↑
                                                    Last reached (dist=3)
```

The **last water cell** the BFS reaches is the **furthest from any land**.

---

## Why Multi-Source BFS?

### ❌ Wrong Approach (Single-source from water)
```python
# Start from one water cell
queue.append((0, 1, 0))
# Problem: We'd need to do BFS from EACH water cell separately
# to find its distance to nearest land
# Time: O(n⁴) or need Dijkstra
```

### ✅ Right Approach (Multi-source from all lands)
```python
# Start from ALL lands simultaneously
for i in range(row):
    for j in range(col):
        if grid[i][j] == 1:
            queue.append((i, j, 0))
```
- Naturally computes distance from each cell to **nearest** land
- Single pass through the grid
- Last cell visited = furthest from any land
- Time: O(n²)

---

## Pattern Recognition

**When to use Multi-Source BFS:**

| Trigger Question | Example | Pattern |
|------------------|---------|---------|
| "Distance from each cell to nearest X?" | Nearest land, nearest 0, nearest bomb | Multi-source from all X |
| "Furthest from nearest X?" | Furthest from land, safest spot | Multi-source → find max distance |
| "Time to infect all?" | Rotting oranges, virus spread | Multi-source → track time |

**Key insight**: If problem asks for "distance to nearest," expand from the nearest targets.

---

## Similar Problems

1. **LeetCode 994** (Rotting Oranges) — Multi-source BFS
   - Start from all rotten oranges, find time to rot all fresh ones
   
2. **LeetCode 542** (01 Matrix) — Multi-source BFS
   - Find distance from each cell to nearest 0
   
3. **LeetCode 490** (The Maze) — BFS with state tracking
   - Find if you can reach destination

4. **LeetCode 1091** (Shortest Path in Binary Matrix) — Multi-source
   - Find shortest path from multiple sources

---

## Template for Multi-Source BFS

```python
def multiSourceBFS(grid):
    queue = deque()
    visited = set()
    
    # 1. Initialize: Add ALL source cells
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == SOURCE:
                queue.append((i, j, 0))
                visited.add((i, j))
    
    # 2. Check edge cases
    if len(queue) == 0:
        return -1
    
    result = 0
    directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
    
    # 3. Expand simultaneously from all sources
    while queue:
        r, c, dist = queue.popleft()
        result = max(result, dist)
        
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if isValid(nr, nc) and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, dist + 1))
    
    return result
```

---

## Common Mistakes

1. ❌ Starting from water cells instead of land
   - ✅ Start from what you want to measure distance TO

2. ❌ Updating `maxDist` after dequeuing any cell
   - ✅ Update only when you find a water cell (the answer cells)

3. ❌ Using `and` instead of `or` for edge case
   - ✅ `if not grid or not grid[0]:` (if either is empty)

4. ❌ Using single-source BFS
   - ✅ Initialize queue with ALL source cells for multi-source

---

## Key Takeaway

**Multi-source BFS = "Expand from all targets simultaneously to compute distance to nearest target efficiently in a single pass."**

When you see "distance to nearest," think multi-source immediately.
