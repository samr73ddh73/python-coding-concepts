# DP on Grids: Patterns & When to Use

## What is DP on Grids?

DP on grids is used when:
- You have a 2D grid
- You need to count paths, find optimal values, or check reachability
- Movement is restricted (usually only right/down, or 4 directions)
- Choices at each cell affect future possibilities
- Subproblems overlap (different paths to same cell)

---

## DP on Grids vs Graph Problems: Key Differences

### ❌ Why BFS/DFS (Graph) Doesn't Work Here

**Graph problems** (BFS/DFS) are for:
```
"Find a path" → ONE answer
"Find shortest path" → ONE answer (or one property)
"Check if reachable" → YES/NO answer
"Find all nodes" → Set of nodes

You DON'T care about counting all possible paths
```

**Example: Simple Unique Paths (3×3 grid)**

BFS approach:
```python
queue = deque([(0,0)])
visited = set()

while queue:
    i, j = queue.popleft()
    if (i,j) == (2,2):
        return "found"  # ← Only ONE answer!
    
    for di, dj in directions:
        ni, nj = i+di, j+dj
        if valid and not visited:
            visited.add((ni, nj))  # Mark as visited
            queue.append((ni, nj))

return "not found"
```

**Problem**: BFS marks cells as **visited** to prevent cycles and infinite loops.
```
Path 1: (0,0) → (0,1) → (0,2) → (1,2) → (2,2)
Path 2: (0,0) → (0,1) → (1,1) → (1,2) → (2,2)

BFS execution:
  Process (0,0): Add (0,1) and (1,0), mark both visited
  Process (0,1): Add (0,2) and (1,1), mark both visited
  Process (1,0): Try to add (1,1), but it's VISITED, skip!
  
Result: Path 2 is NEVER explored because (1,1) already marked visited
```

BFS finds **ONE** path, not **COUNT** of all paths.

---

### ✅ Why DP on Grids Works

**DP on grids** is for:
```
"Count all paths" → SUM of all solutions
"Find minimum/maximum value" → OPTIMIZE across all options
"Count ways" → Combine subproblem counts

You CARE about combining solutions from all paths
```

**DP approach (same problem)**:

```python
memo = {}

def dp(i, j):
    if reached_end:
        return 1  # One way
    
    # Return COUNT of paths from this cell
    return dp(i+1, j) + dp(i, j+1)  # Both paths counted!
```

**Why it works**:
```
(1,1) is reachable from (0,1) AND (1,0)
We DON'T mark it visited
We COMPUTE it twice, but memoize the result

First time: compute dp(1,1) from (0,1)
Second time: dp(1,1) from (1,0) → cache hit, return memo[1,1]

Both paths are COUNTED because we don't block revisits!
```

---

## Core Difference Summary

| Aspect | Graph (BFS/DFS) | DP on Grids |
|--------|-----------------|-------------|
| **Goal** | Find path, check reachability | Count/optimize all paths |
| **Visited tracking** | ✅ Required (prevent cycles) | ❌ NOT needed (memoize results) |
| **Answer type** | YES/NO or ONE solution | SUM or COMBINE solutions |
| **What we track** | Which cells visited | How many ways to each cell |
| **Revisits** | ❌ Blocked by visited | ✅ Allowed (memoized) |
| **Problem type** | Finding/searching | Counting/optimizing |

---

## Visual: BFS vs DP

### BFS (Graph) - Finding Path

```
Grid:
S 0 0
0 0 0
0 0 E

BFS explores:
S → (adjacent) → (adjacent) → E

Mark each cell visited (don't go back)
Result: Found path (yes/no) or shortest path

     S
    / \
   X   X (one branch taken, other ignored)
   |
   X
   |
   E
```

### DP (Grids) - Counting Paths

```
Grid:
S 0 0
0 0 0
0 0 E

DP explores ALL paths:
Path 1: S → right → right → down → down → E
Path 2: S → down → right → right → down → E
Path 3: S → right → down → right → down → E
... (more paths)

Result: Total count of all paths

Both branches taken at every step!
```

---

## Why Not Use BFS with "Don't Mark Visited"?

**You might think**: "Just don't use visited, and BFS will explore all paths"

```python
queue = deque([(0,0)])
# NO visited set!

while queue:
    i, j = queue.popleft()
    if (i,j) == (2,2):
        ans += 1
    
    for di, dj in directions:
        ni, nj = i+di, j+dj
        if valid:
            queue.append((ni, nj))  # No visited check!
```

**Problem**: INFINITE LOOP!

```
(0,0) adds (0,1) and (1,0)
(0,1) adds (0,2) and (1,1)
(1,0) adds (0,0) and (1,1)
(0,0) adds (0,1) and (1,0)  ← Already in queue!
(0,1) adds (0,2) and (1,1)  ← Already in queue!

Queue grows infinitely: [(0,1), (1,0), (0,2), (1,1), (0,0), (0,1), (1,0), ...]

Never terminates!
```

**This is why you need DP (memoization) or DFS (with recursion stack)**

---

## When to Use Each

### Use BFS When:
```
✅ "Find shortest path" (unweighted)
✅ "Check if reachable"
✅ "Find minimum distance to any node"
✅ "Level-order traversal"

Example: Word Ladder, Shortest Path in Binary Matrix, Rotting Oranges
```

### Use DP When:
```
✅ "Count all paths"
✅ "Find minimum/maximum cost across all paths"
✅ "Find number of ways to make X"
✅ Overlapping subproblems in grid

Example: Unique Paths, Min Path Sum, Cherry Pickup, Number of ways
```

### Use DFS When:
```
✅ "Explore all possibilities" (backtracking)
✅ "Check all paths"
✅ "Detect cycles"
✅ "Generate permutations/combinations"

Example: Word Search, Path with Maximum Gold, N-Queens
```

---

## Recognition: When is it DP on Grids?

Ask these trigger questions:

### 1️⃣ "Do I have a 2D grid?"
```
YES → Continue to next question
NO  → Not a grid DP problem
```

### 2️⃣ "Do I move through the grid with restricted movements?"
```
Only right/down? → DP on grids
4 directions?    → Could be DP (with more complexity)
Free movement?   → Likely not DP on grids
```

### 3️⃣ "What am I computing?"
```
Count paths?           → DP (counting paths)
Find minimum/maximum?  → DP (optimization)
Check reachability?    → BFS or DFS (not DP)
```

### 4️⃣ "Do paths overlap? (reach same cell multiple ways?)"
```
YES, and I want to COUNT them → DP is ideal
YES, but I only care about ONE property → BFS
NO  → Maybe just backtracking/DFS
```

---

## Common DP on Grids Problems

| Problem | Goal | Why DP, Not BFS |
|---------|------|-----------------|
| **Unique Paths** | Count ways to reach bottom-right | Count ALL paths, not just one |
| **Unique Paths II** | Count paths with obstacles | BFS would find one path, not count |
| **Minimum Path Sum** | Minimize cost to reach end | Combine costs across all paths |
| **Maximal Square** | Find largest square of 1s | Different state definition |
| **Cherry Pickup** | Maximize cherry collection | Two interdependent paths |

---

## DP on Grids: Two Main Approaches

### Approach 1: Bottom-Up (Iterative)

```python
# Fill table systematically (left→right, top→bottom)
dp = [[0] * cols for _ in range(rows)]
dp[0][0] = base_case

for i in range(rows):
    for j in range(cols):
        # Compute based on top and left
        dp[i][j] = combine(dp[i-1][j], dp[i][j-1])

return dp[rows-1][cols-1]
```

**Advantages**:
- No recursion overhead
- Clear iteration order
- Fast in practice

---

### Approach 2: Top-Down (Memoization)

```python
# Recursive with memoization
memo = {}

def dp(i, j):
    if out_of_bounds or obstacle:
        return base_case
    if (i, j) in memo:
        return memo[(i, j)]
    
    result = combine(dp(i+1, j), dp(i, j+1))
    memo[(i, j)] = result
    return result

return dp(0, 0)
```

**Advantages**:
- Only compute reachable cells
- Flexible base case handling
- No visited tracking needed (memoization prevents recomputation)

---

## DP State Definition

### Key Question: What does `dp[i][j]` represent?

```python
# Unique Paths:
# dp[i][j] = "number of ways to reach (i,j) from (0,0)"

# Minimum Path Sum:
# dp[i][j] = "minimum cost to reach (i,j) from (0,0)"

# Maximal Square:
# dp[i][j] = "side length of largest square with (i,j) as bottom-right"
```

**Clear state definition = Clear recurrence**

---

## Recurrence Patterns

### Pattern 1: Counting Paths (Sum Subproblems)

```python
# Paths to (i,j) = paths from top + paths from left
dp[i][j] = dp[i-1][j] + dp[i][j-1]

# Examples: Unique Paths, Unique Paths II
```

### Pattern 2: Optimization (Min/Max Subproblems)

```python
# Minimum cost to (i,j) = min(cost from top, cost from left) + current cost
dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + cost[i][j]

# Examples: Minimum Path Sum, Cherry Pickup
```

---

## Common Pitfalls

### ❌ Pitfall 1: Using BFS Instead of DP for Counting

```python
# ❌ WRONG: BFS
queue = deque([(0,0)])
visited = set()
ans = 0

while queue:
    i, j = queue.popleft()
    if (i,j) == end and (i,j) not in visited:
        ans += 1
    
    # BFS prevents paths from being counted multiple times!
```

### ❌ Pitfall 2: Obstacle Handling in DP

```python
# Wrong:
if grid[i][j] == 1:
    dp[i][j] = dp[i-1][j] + dp[i][j-1]  # Still adds paths!

# Right:
if grid[i][j] == 1:
    dp[i][j] = 0  # Obstacle blocks all paths
else:
    dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

---

## Complexity Analysis

### Time Complexity: O(rows × cols)

Why?
- Visit each cell: O(rows × cols)
- Per cell: O(1) to combine subproblems
- Total: O(rows × cols)

### Space Complexity

Bottom-up: O(rows × cols) for DP table  
Top-down: O(rows × cols) memo + O(rows + cols) recursion depth

---

## Decision Tree: DP on Grids vs BFS vs DFS

```
Is it a grid problem?
├─ NO → Not grid-related
└─ YES:
    Do I need to COUNT all paths or OPTIMIZE?
    ├─ YES → DP ON GRIDS
    │  └─ Restricted movement (right/down)?
    │     ├─ YES → Simple DP ✓
    │     └─ NO → Complex DP (4 directions)
    └─ NO:
        Do I need SHORTEST PATH or REACHABILITY?
        ├─ YES → BFS ✓
        └─ NO:
            Do I need to EXPLORE ALL and BACKTRACK?
            ├─ YES → DFS ✓
            └─ NO → Re-evaluate problem
```

---

## Template: DP on Grids (Top-Down)

```python
def gridDP(grid):
    rows, cols = len(grid), len(grid[0])
    memo = {}
    
    def dp(i, j):
        # Base cases
        if i >= rows or j >= cols:
            return base_out_of_bounds
        
        if is_obstacle(grid[i][j]):
            return base_obstacle
        
        if i == rows-1 and j == cols-1:
            return base_destination
        
        # Check memo
        if (i, j) in memo:
            return memo[(i, j)]
        
        # Recurrence: combine subproblems
        result = combine(dp(i+1, j), dp(i, j+1))
        memo[(i, j)] = result
        return result
    
    return dp(0, 0)
```

---

## Key Takeaways

1. **DP on grids = Count/optimize all paths across overlapping subproblems**
2. **BFS/DFS = Find ONE path or check reachability (prevents revisits)**
3. **Memoization = Allows revisits for counting (BFS visited prevents this)**
4. **Complexity = O(rows × cols)** in most cases
5. **Top-down easier, bottom-up faster**

**When you see "count paths" or "find minimum across paths" in a grid → Use DP, not BFS!**
