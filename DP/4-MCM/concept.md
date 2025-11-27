# Matrix Chain Multiplication (MCM) Pattern

## When to Use
Use this pattern when you need to **partition** something to find the optimal solution.

## Problem Statement
Find the minimum cost for multiplying n matrices.

Given: A × B × C × D (matrices)

**Key Insight**: The order of multiplication matters!
- (A×B)×(C×D×E)
- (A×B×C)×(D×E)
- Different partitions → different costs

## Cost Calculation
Multiplying two matrices:
```
Matrix(a×b) × Matrix(b×c) = Matrix(a×c)
Cost = a × b × c operations
```

## MCM Pattern (5 Steps)

### 1. Find i and j
- `i` = start index (usually 0 or 1)
- `j` = end index (usually n-1 or n)

### 2. Base Condition
```python
if i >= j:  # Single matrix or invalid range
    return 0
```

### 3. Loop with k (Partition Point)
```python
for k in range(i, j):
    # k partitions the array: [i...k] and [k+1...j]
```

### 4. Calculate Temp Answer
```python
temp_ans = solve(i, k) + solve(k+1, j) + cost_of_merging
```

Where:
- `solve(i, k)` = cost of left partition
- `solve(k+1, j)` = cost of right partition
- `cost_of_merging` = cost to combine the two results

### 5. Final Answer
```python
min_ans = min(min_ans, temp_ans)  # For minimization
# OR
max_ans = max(max_ans, temp_ans)  # For maximization
```

## MCM Template Code

```python
def mcm(arr, i, j):
    # Step 2: Base condition
    if i >= j:
        return 0

    min_ans = float('inf')

    # Step 3: Loop with k (try all partition points)
    for k in range(i, j):
        # Step 4: Calculate temp answer
        # Left partition + Right partition + Merge cost
        temp_ans = (mcm(arr, i, k) +
                   mcm(arr, k+1, j) +
                   arr[i-1] * arr[k] * arr[j])

        # Step 5: Update final answer
        min_ans = min(min_ans, temp_ans)

    return min_ans
```

## Optimization: Memoization

```python
def mcm_memo(arr, i, j, dp):
    # Base condition
    if i >= j:
        return 0

    # Check memo
    if dp[i][j] != -1:
        return dp[i][j]

    min_ans = float('inf')

    # Try all partitions
    for k in range(i, j):
        temp_ans = (mcm_memo(arr, i, k, dp) +
                   mcm_memo(arr, k+1, j, dp) +
                   arr[i-1] * arr[k] * arr[j])
        min_ans = min(min_ans, temp_ans)

    dp[i][j] = min_ans
    return min_ans

# Initialize
n = len(arr)
dp = [[-1] * n for _ in range(n)]
result = mcm_memo(arr, 1, n-1, dp)
```

## Example: Matrix Dimensions

Given matrices: A(10×20), B(20×30), C(30×40)

Array representation: `[10, 20, 30, 40]`
- arr[0]=10, arr[1]=20, arr[2]=30, arr[3]=40
- A = arr[0]×arr[1]
- B = arr[1]×arr[2]
- C = arr[2]×arr[3]

**Partitions:**
1. (A×B)×C:
   - A×B cost: 10×20×30 = 6000
   - Result×C cost: 10×30×40 = 12000
   - Total: 18000

2. A×(B×C):
   - B×C cost: 20×30×40 = 24000
   - A×Result cost: 10×20×40 = 8000
   - Total: 32000

Optimal: (A×B)×C = 18000 ✓

## Time Complexity

**Without Memoization**: O(2^n) - exponential
**With Memoization**: O(n³)
- States: O(n²) (all i,j pairs)
- Work per state: O(n) (loop through k)

**Space**: O(n²) for DP table

## Common MCM Variations

1. **Matrix Chain Multiplication**: Minimize multiplication cost
2. **Palindrome Partitioning**: Minimize cuts to make all palindromes
3. **Boolean Parenthesization**: Count ways to parenthesize to get True
4. **Egg Dropping**: Minimize worst-case drops
5. **Burst Balloons**: Maximize coins from bursting balloons

## Key Takeaways

✓ Pattern: Partition at every possible point and take optimal
✓ Always involves a loop through partition points (k)
✓ Combine results from left and right partitions
✓ Use memoization to avoid recomputation
✓ Base case: when partition is invalid or trivial
