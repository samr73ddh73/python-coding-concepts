# Time Complexity Analysis for Dynamic Programming

## Table of Contents
1. [General Framework](#general-framework)
2. [0/1 Knapsack Problem](#01-knapsack-problem)
3. [Common DP Patterns](#common-dp-patterns)
4. [How to Analyze Any DP Problem](#how-to-analyze-any-dp-problem)

---

## General Framework

### Formula for DP Time Complexity:
```
Time Complexity = (Number of Unique States) × (Work per State)
```

### Steps to Calculate:
1. **Identify state variables** (parameters that change in recursion)
2. **Count range of each variable**
3. **Multiply ranges** to get total states
4. **Analyze work done per state** (excluding recursive calls)
5. **Result = States × Work**

---

## 0/1 Knapsack Problem

### Problem Statement
Given weights and profits of n items, find maximum profit for a knapsack of capacity W.

### Top-Down Memoization (Recursive)

```python
def knapsack(wt, profit, n, cap):
    # Base case
    if cap <= 0 or n == 0:
        return 0

    # Check cache
    if (cap, n) in memo:
        return memo[(cap, n)]

    # Take or skip
    take = 0
    if wt[n-1] <= cap:
        take = knapsack(wt, profit, n-1, cap-wt[n-1]) + profit[n-1]
    skip = knapsack(wt, profit, n-1, cap)

    # Store and return
    memo[(cap, n)] = max(take, skip)
    return memo[(cap, n)]
```

**Time Complexity Analysis:**

| Step | Analysis | Result |
|------|----------|--------|
| 1. State variables | `n` (items) and `cap` (capacity) | 2 variables |
| 2. Range of n | 0 to n | n+1 values |
| 3. Range of cap | 0 to capacity | capacity+1 values |
| 4. Total states | (n+1) × (capacity+1) | **O(n × capacity)** |
| 5. Work per state | Dictionary lookup O(1), max O(1), arithmetic O(1) | **O(1)** |
| **Final** | **States × Work** | **O(n × capacity)** |

**Space Complexity:**
- Memoization table: `O(n × capacity)` - stores all unique states
- Recursion stack: `O(n)` - maximum depth is n
- **Total: O(n × capacity) + O(n) = O(n × capacity)**

**Without Memoization:**
- Each call makes 2 recursive calls → branching factor of 2
- Maximum depth of n → **O(2^n)** exponential time
- Memoization reduces this from exponential to polynomial!

---

### Bottom-Up Tabulation (Iterative)

```python
def knapsack_dp(wt, profit, capacity):
    n = len(wt)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):              # n iterations
        for c in range(capacity + 1):       # capacity iterations
            dp[i][c] = dp[i-1][c]
            if wt[i-1] <= c:
                dp[i][c] = max(dp[i][c], profit[i-1] + dp[i-1][c - wt[i-1]])

    return dp[n][capacity]
```

**Time Complexity Analysis:**

| Component | Count | Work | Total |
|-----------|-------|------|-------|
| Outer loop (items) | n | - | n iterations |
| Inner loop (capacity) | capacity | O(1) per iteration | capacity iterations |
| Work per cell | Array access, max comparison | O(1) | - |
| **Total** | **n × capacity iterations** | **O(1) each** | **O(n × capacity)** |

**Space Complexity:**
- DP table: `(n+1) × (capacity+1)` → **O(n × capacity)**
- No recursion stack → saves O(n) compared to top-down

---

### Space-Optimized (1D Array)

```python
def knapsack_optimized(wt, profit, capacity):
    dp = [0] * (capacity + 1)

    for i in range(len(wt)):                    # n iterations
        for c in range(capacity, wt[i]-1, -1):  # up to capacity iterations
            dp[c] = max(dp[c], profit[i] + dp[c - wt[i]])

    return dp[capacity]
```

**Time Complexity:**
- Outer loop: n iterations
- Inner loop: up to capacity iterations
- Work per iteration: O(1)
- **Total: O(n × capacity)** (same as 2D version)

**Space Complexity:**
- Only one array of size capacity: **O(capacity)** ✨
- No recursion stack
- **Major improvement from O(n × capacity) to O(capacity)!**

**Why traverse backwards?**
```python
# Forward traversal (WRONG):
for c in range(wt[i], capacity + 1):
    dp[c] = max(dp[c], profit[i] + dp[c - wt[i]])
    # dp[c - wt[i]] might already be updated for current item!
    # This allows taking the same item multiple times (unbounded knapsack)

# Backward traversal (CORRECT for 0/1):
for c in range(capacity, wt[i] - 1, -1):
    dp[c] = max(dp[c], profit[i] + dp[c - wt[i]])
    # dp[c - wt[i]] is guaranteed to be from previous row (previous item)
```

---

## Comparison Table

| Approach | Time | Space | Recursion Stack | Best For |
|----------|------|-------|-----------------|----------|
| **Naive Recursion** | O(2^n) | O(n) | Yes (O(n)) | Never use in production |
| **Top-Down Memo** | O(n × capacity) | O(n × capacity) | Yes (O(n)) | Intuitive, easy to code |
| **Bottom-Up 2D** | O(n × capacity) | O(n × capacity) | No | Clear logic, easy to debug |
| **Bottom-Up 1D** | O(n × capacity) | **O(capacity)** | No | **Best space optimization** |

---

## Common DP Patterns

### Pattern 1: Single Variable DP
**Examples:** Fibonacci, Climbing Stairs, House Robber

```python
# Fibonacci
def fib(n):
    if n <= 1: return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

**Time:** O(n) - one loop from 0 to n
**Space:** O(n) - can be optimized to O(1) with two variables

---

### Pattern 2: Two Variable DP
**Examples:** Longest Common Subsequence, Edit Distance, Knapsack

```python
# Longest Common Subsequence
def lcs(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]
```

**Time:** O(m × n) - two nested loops
**Space:** O(m × n) - can be optimized to O(min(m, n))

**State variables:** `i` (position in s1), `j` (position in s2)
**States:** m × n
**Work per state:** O(1)

---

### Pattern 3: Partition DP
**Examples:** Palindrome Partitioning, Matrix Chain Multiplication

```python
# Minimum cost to multiply chain of matrices
def matrix_chain(dims):
    n = len(dims) - 1
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):              # O(n)
        for i in range(n - length + 1):         # O(n)
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):                # O(n)
                cost = dp[i][k] + dp[k+1][j] + dims[i]*dims[k+1]*dims[j+1]
                dp[i][j] = min(dp[i][j], cost)

    return dp[0][n-1]
```

**Time:** O(n³) - three nested loops
**Space:** O(n²)

---

### Pattern 4: String DP with Multiple Decisions
**Examples:** Regular Expression Matching, Wildcard Matching

```python
# Edit Distance
def edit_distance(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases
    for i in range(m + 1): dp[i][0] = i
    for j in range(n + 1): dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j],      # delete
                    dp[i][j-1],      # insert
                    dp[i-1][j-1]     # replace
                )

    return dp[m][n]
```

**Time:** O(m × n)
**Space:** O(m × n) - can be optimized to O(min(m, n))

---

## How to Analyze Any DP Problem

### Step-by-Step Checklist:

#### 1. Identify the Approach
- [ ] Is it top-down (recursion + memoization)?
- [ ] Is it bottom-up (tabulation)?
- [ ] Is it space-optimized?

#### 2. Find State Variables
- [ ] What parameters change in the recursion/iteration?
- [ ] What do we need to uniquely identify a subproblem?

#### 3. Count States
- [ ] What is the range of each state variable?
- [ ] Multiply ranges to get total states

#### 4. Analyze Work Per State
- [ ] What operations happen inside each state? (exclude recursive calls)
- [ ] Are there loops inside the state computation?
- [ ] Dictionary/array operations are usually O(1)

#### 5. Calculate Space
- [ ] How big is the memoization table/DP array?
- [ ] Is there a recursion stack? (top-down only, usually O(n) or O(max_depth))
- [ ] Can we optimize by using fewer dimensions?

---

### Example Analysis: Coin Change

**Problem:** Minimum coins needed to make amount `n` with given coin denominations.

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):           # State variable
        for coin in coins:                    # Decision loop
            if i >= coin:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float('inf') else -1
```

**Analysis:**
1. **Approach:** Bottom-up tabulation
2. **State variables:** `i` (current amount) → 1 variable
3. **Count states:** 0 to amount → **O(amount)** states
4. **Work per state:** Inner loop over coins → **O(len(coins))** work
5. **Time complexity:** O(amount) × O(len(coins)) = **O(amount × coins)**
6. **Space complexity:** dp array → **O(amount)**

---

## Quick Reference: Common Complexities

| DP Problem | Time | Space | Pattern |
|------------|------|-------|---------|
| Fibonacci | O(n) | O(1)* | 1D DP |
| Climbing Stairs | O(n) | O(1)* | 1D DP |
| House Robber | O(n) | O(1)* | 1D DP |
| Coin Change | O(amount × coins) | O(amount) | 1D DP with inner loop |
| 0/1 Knapsack | O(n × capacity) | O(capacity)* | 2D → 1D optimization |
| Unbounded Knapsack | O(n × capacity) | O(capacity) | 1D DP |
| LCS | O(m × n) | O(min(m,n))* | 2D → 1D optimization |
| Edit Distance | O(m × n) | O(min(m,n))* | 2D → 1D optimization |
| Longest Increasing Subsequence | O(n²) or O(n log n) | O(n) | 1D or Binary Search |
| Matrix Chain Multiplication | O(n³) | O(n²) | Partition DP |
| Palindrome Partitioning | O(n³) | O(n²) | Partition DP |
| Word Break | O(n² × m) | O(n) | String DP |

\* With space optimization

---

## FAANG Interview Tips

### What to Say:

**Before coding:**
> "I'll use dynamic programming. Let me identify the states first..."
> "This has optimal substructure because..."
> "I can see overlapping subproblems when..."

**During coding:**
> "The state variables are [x, y]..."
> "Each state represents..."
> "This gives us O(n × m) states with O(1) work per state..."

**After coding:**
> "The time complexity is O(...) because we have ... states and ... work per state."
> "For space, we use O(...) for the DP table plus O(...) for recursion stack."
> "We can optimize space to O(...) by using a rolling array / 1D array."

### Common Follow-ups:

1. **"Can you optimize space?"**
   - Convert 2D to 1D array
   - Use rolling array (keep only last row/column)

2. **"What if constraints change?"**
   - Larger n → may need space optimization
   - Negative numbers → adjust base cases
   - Different constraints → might change approach

3. **"Can you print the actual solution, not just the value?"**
   - Add backtracking after computing DP table
   - Or store decisions during DP computation

4. **"What's the space-time tradeoff?"**
   - Less space → might need recomputation
   - More space → faster lookups

---

## Practice Problems by Pattern

### 1D DP (O(n) time):
- Climbing Stairs
- Min Cost Climbing Stairs
- House Robber
- Decode Ways

### 2D DP (O(n²) or O(m×n) time):
- Unique Paths
- Minimum Path Sum
- Longest Common Subsequence
- Edit Distance
- 0/1 Knapsack

### Partition DP (O(n³) time):
- Matrix Chain Multiplication
- Burst Balloons
- Palindrome Partitioning II

### With Inner Loop (O(n × k) time):
- Coin Change
- Perfect Squares
- Jump Game II

---

## Summary Checklist

When analyzing DP time complexity, always:

- ✅ Identify all state variables
- ✅ Count the range of each variable
- ✅ Multiply ranges for total states
- ✅ Analyze work per state (excluding recursion)
- ✅ Consider recursion stack for space
- ✅ Think about space optimization opportunities

**Remember:** Memoization transforms exponential O(2^n) to polynomial O(n × k) by ensuring each state is computed only once!

---

*Last updated: For FAANG interview preparation*
*Related: 0-1-knapsack/top-down.py, bottom-up.py, space-optimized.py*
