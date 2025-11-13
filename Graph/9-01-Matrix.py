# https://leetcode.com/problems/01-matrix/description/

"""
================================================================================
PATTERN: Multi-Source BFS (Simultaneous BFS from multiple starting points)
================================================================================

PROBLEM:
Given an m x n binary matrix mat, return the distance of the nearest 0 for each cell.
The distance between two adjacent cells is 1.

KEY INSIGHT - REVERSE THE THINKING:
❌ WRONG: For each cell with 1, find nearest 0 (BFS from each cell)
   - Time: O(n²m²) - Running BFS from each of n×m cells → TLE

✅ CORRECT: Start from ALL 0s simultaneously and propagate distances outward
   - Time: O(n×m) - Each cell visited exactly once
   - Instead of asking "where's the nearest 0?", ask "how far can we reach from all 0s?"

WHY MULTI-SOURCE BFS?
- All 0s are at distance 0 from themselves
- Cells adjacent to 0s are at distance 1
- Cells adjacent to distance-1 cells are at distance 2, etc.
- BFS guarantees we visit cells in increasing order of distance
- First time we reach a cell = shortest distance (BFS property)

ALGORITHM:
1. Initialize: Add all 0s to queue (multiple sources), mark 1s as infinity
2. BFS: For each cell popped, update unvisited neighbors with distance + 1
3. Add updated neighbors to queue
4. Continue until queue is empty

TIME COMPLEXITY: O(n × m)
- Initialization: O(n×m) to scan matrix and add 0s to queue
- BFS: Each cell added to queue at most once → O(n×m)
- Each cell processes 4 neighbors → O(4×n×m) = O(n×m)
- Total: O(n×m)

SPACE COMPLEXITY: O(n × m)
- Queue: In worst case (all 0s or checkerboard), queue can hold O(n×m) cells
- Can reuse input matrix or use separate result array

EDGE CASES:
1. All 0s → return as-is
2. Single 0 → BFS propagates Manhattan distances
3. Single cell → return as-is
4. One row/column → linear propagation

OPTIMIZATION:
- Can reuse input matrix instead of separate result array
- No need to store level in queue - matrix value itself tracks distance
- Condition `mat[nx][ny] > mat[x][y] + 1` acts as visited check

PYTHON INTERNALS:
- deque() for O(1) append/popleft (list.pop(0) is O(n))
- float('inf') for unvisited marker
"""


# ============================================================================
# CORRECT SOLUTION: Multi-Source BFS (Optimal)
# ============================================================================
class SolutionOptimal:
    """
    Optimal approach without storing level in queue
    TIME: O(n×m) | SPACE: O(n×m)
    """
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        if not mat or not mat[0]:
            return mat

        n, m = len(mat), len(mat[0])
        queue = deque()

        # Step 1: Add ALL 0s to queue (multi-source), mark 1s as infinity
        for i in range(n):
            for j in range(m):
                if mat[i][j] == 0:
                    queue.append((i, j))  # All 0s start at distance 0
                else:
                    mat[i][j] = float('inf')  # Mark 1s as unvisited

        # Step 2: Multi-source BFS - propagate distances from all 0s
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            x, y = queue.popleft()

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < n and 0 <= ny < m:
                    # Update only if found shorter distance
                    # mat[x][y] already contains distance for current cell
                    if mat[nx][ny] > mat[x][y] + 1:
                        mat[nx][ny] = mat[x][y] + 1
                        queue.append((nx, ny))

        return mat


# ============================================================================
# ALTERNATIVE: With Explicit Level Tracking
# ============================================================================
class SolutionWithLevel:
    """
    Store distance explicitly in queue
    TIME: O(n×m) | SPACE: O(n×m) - slightly more memory

    Use this pattern when:
    - Need to track level for specific logic
    - Dealing with weighted graphs
    - Need to know level during processing
    """
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        n, m = len(mat), len(mat[0])
        queue = deque()
        res = [[float('inf')] * m for _ in range(n)]
        visited = set()

        # Add all 0s with distance 0
        for i in range(n):
            for j in range(m):
                if mat[i][j] == 0:
                    queue.append((i, j, 0))  # (row, col, distance)
                    res[i][j] = 0
                    visited.add((i, j))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            x, y, dist = queue.popleft()

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < n and 0 <= ny < m and (nx, ny) not in visited:
                    res[nx][ny] = dist + 1
                    visited.add((nx, ny))
                    queue.append((nx, ny, dist + 1))

        return res


"""
VISUAL EXAMPLE - How Multi-Source BFS Works:

Initial: [[0,0,0],    Step 1: Add all 0s      Step 2: BFS propagates
         [0,1,0],     Queue has 5 zeros       distances outward
         [1,1,1]]
                      [[0,  0,  0  ],          [[0,0,0],
                       [0, inf, 0  ],           [0,1,0],
                       [inf,inf,inf]]           [1,2,1]]

BFS naturally visits: distance 0 → distance 1 → distance 2
This guarantees shortest path!
"""
