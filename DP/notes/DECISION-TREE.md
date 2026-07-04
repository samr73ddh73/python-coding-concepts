# 🌳 DP Decision Tree

> When to use DP vs BFS vs DFS for grid problems

---

## Decision Tree: DP on Grids vs BFS vs DFS

```
Is it a grid problem?
├─ NO → Not grid-related
└─ YES:
    Do I need to COUNT all paths or OPTIMIZE?
    ├─ YES → DP ON GRIDS ✓
    │  └─ Restricted movement (right/down)?
    │     ├─ YES → Simple DP (2-directional)
    │     └─ NO → Complex DP (4+ directions)
    └─ NO:
        Do I need SHORTEST PATH or REACHABILITY?
        ├─ YES → BFS ✓
        └─ NO:
            Do I need to EXPLORE ALL and BACKTRACK?
            ├─ YES → DFS ✓
            └─ NO → Re-evaluate problem
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

## When to Use Each

### Use BFS When:
```
✅ "Find shortest path" (unweighted)
✅ "Check if reachable"
✅ "Find minimum distance to any node"
✅ "Level-order traversal"
✅ "Rotten oranges" (multi-source propagation)

Example Problems: Word Ladder, Shortest Path in Binary Matrix, Rotting Oranges
```

### Use DP On Grids When:
```
✅ "Count all paths"
✅ "Find minimum/maximum cost across all paths"
✅ "Find number of ways to make X"
✅ Overlapping subproblems in grid
✅ You DON'T want to block revisits

Example Problems: Unique Paths, Min Path Sum, Cherry Pickup, Number of ways
```

### Use DFS When:
```
✅ "Explore all possibilities" (backtracking)
✅ "Check all paths"
✅ "Detect cycles"
✅ "Generate permutations/combinations"
✅ Need explicit backtracking

Example Problems: Word Search, Path with Maximum Gold, N-Queens
```

---

## Key Insight: Why NOT BFS for Counting?

**The Problem:**
```python
# ❌ Wrong approach: BFS without visited
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

**Result: INFINITE LOOP!**
- Without visited: Queue grows infinitely with duplicate cells
- With visited: Only ONE path is counted (not all)

**Solution: Use DP with memoization** (allows revisits but avoids recomputation)

---

## DP on Grids: Template

### Approach 1: Bottom-Up (Iterative)

```python
def gridDP(grid):
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = base_case
    
    for i in range(rows):
        for j in range(cols):
            # Compute based on top and left (or other directions)
            dp[i][j] = combine(dp[i-1][j], dp[i][j-1])
    
    return dp[rows-1][cols-1]
```

**Advantages**: Fast, no recursion overhead

### Approach 2: Top-Down (Memoization)

```python
def gridDP(grid):
    memo = {}
    
    def dp(i, j):
        # Base cases
        if out_of_bounds or obstacle:
            return base_case
        
        if i == rows-1 and j == cols-1:
            return destination_value
        
        # Check memo
        if (i, j) in memo:
            return memo[(i, j)]
        
        # Recurrence: combine subproblems
        result = combine(dp(i+1, j), dp(i, j+1))
        memo[(i, j)] = result
        return result
    
    return dp(0, 0)
```

**Advantages**: Flexible, only compute needed cells

---

## DP State Definition: The Critical Step

**What does `dp[i][j]` represent?**

| Problem | State Definition | Recurrence |
|---------|---|---|
| **Unique Paths** | "# ways to reach (i,j) from (0,0)" | `dp[i][j] = dp[i-1][j] + dp[i][j-1]` |
| **Min Path Sum** | "Minimum cost to reach (i,j)" | `dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + cost[i][j]` |
| **Maximal Square** | "Side length of largest square at (i,j)" | Special formula |
| **Cherry Pickup** | "Max cherries with 2 paths" | Complex combining |

**Key:** Clear state definition = Clear recurrence = Easy implementation

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

## Complexity Analysis

### Time Complexity: O(rows × cols)

- Visit each cell once
- Per cell: O(1) to combine subproblems
- Total: **O(rows × cols)**

### Space Complexity

- **Bottom-up**: O(rows × cols) for DP table (can optimize to O(cols) with rolling array)
- **Top-down**: O(rows × cols) memo + O(rows + cols) recursion depth

---

## Common Pitfalls

### ❌ Pitfall 1: Using BFS Instead of DP for Counting

```python
# WRONG: BFS
queue = deque([(0,0)])
visited = set()

while queue:
    # BFS prevents paths from being counted multiple times!
```

### ❌ Pitfall 2: Obstacle Handling in DP

```python
# Wrong:
if grid[i][j] == 1:
    dp[i][j] = dp[i-1][j] + dp[i][j-1]  # Still adds!

# Right:
if grid[i][j] == 1:
    dp[i][j] = 0  # Block all paths through obstacle
else:
    dp[i][j] = dp[i-1][j] + dp[i][j-1]
```

### ❌ Pitfall 3: Wrong Base Cases

```python
# Make sure base cases are clear:
# - Out of bounds?
# - Obstacles?
# - Starting cell?
# - Destination cell?
```

---

## Recognition Checklist

When you see a grid problem, ask:

1. ✅ Do I have a 2D grid? (YES → continue)
2. ✅ Do I move with restricted movements? (right/down or 4-dir)
3. ✅ What am I computing? (Count? Optimize? Check reachable?)
4. ✅ Do paths overlap (reach same cell multiple ways)?

**If counting/optimizing overlapping paths → DP on Grids**

---

## Interview Tips

1. **Identify the problem type first** (count vs find vs check)
2. **Define your DP state clearly** (what does dp[i][j] mean?)
3. **Write the recurrence relation** (how do subproblems combine?)
4. **Implement bottom-up first** (easier to debug)
5. **Optimize space if asked** (rolling array technique)
6. **Test edge cases** (empty, single cell, all obstacles, no obstacles)

---

## Quick Reference

| Decision | Answer | Algorithm |
|----------|--------|-----------|
| Grid problem? | YES | Continue |
| Count/Optimize? | YES | **DP on Grids** |
| Count/Optimize? | NO | Continue |
| Shortest/Reachable? | YES | **BFS** |
| Shortest/Reachable? | NO | Continue |
| Explore all + Backtrack? | YES | **DFS** |

---

*For detailed implementations, see the pattern files and problem examples in this folder.*
