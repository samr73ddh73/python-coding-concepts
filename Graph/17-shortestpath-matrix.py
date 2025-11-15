"""
================================================================================
PATTERN: Shortest Path in Binary Matrix using BFS
================================================================================

PROBLEM:
Given an n x n binary matrix grid, return the length of the shortest clear path
in the matrix. If there is no clear path, return -1.

A clear path:
- Starts at grid[0][0] and ends at grid[n-1][n-1]
- All visited cells are 0
- Can move in 8 DIRECTIONS (including diagonals)
- Path length = number of cells visited

KEY INSIGHT:
This is an UNWEIGHTED graph shortest path problem → Use BFS!
- BFS guarantees shortest path in unweighted graphs
- First time we reach destination = shortest path (BFS level-order property)
- Need 8-DIRECTIONAL movement (not just 4!)

ALGORITHM:
1. Early validation: Check if start/end cells are blocked (return -1)
2. BFS from (0,0) with distance tracking
3. For each cell, explore all 8 neighbors
4. EARLY TERMINATE when reaching (n-1, n-1) - no need to explore further!
5. If destination never reached → return -1

================================================================================
TIME COMPLEXITY: O(n²)
================================================================================
- n x n grid → O(n²) cells
- Each cell visited at most once: O(n²)
- For each cell, check 8 neighbors: O(8) = O(1)
- Total: O(n²)

SPACE COMPLEXITY: O(n²)
- Visited set: O(n²) in worst case (all cells are 0)
- Queue: O(n²) in worst case (BFS frontier can be large)
- Total: O(n²)

================================================================================
COMMON MISTAKES (YOUR CODE HAD THESE!):
================================================================================
1. ❌ Using only 6 directions instead of 8 (missing (-1,1) and (1,-1) diagonals)
   - Your line 9 had: [(0,-1), (-1, 0), (-1,-1), (1, 0), (0,1), (1, 1)]
   - Missing: (-1, 1) top-right and (1, -1) bottom-left

2. ❌ Tracking maxD (max distance to ANY cell) instead of distance to destination
   - Your lines 14, 24, 26: maxD = max(maxD, dist+1) then return maxD
   - This returns the LONGEST distance to any reachable cell, NOT distance to (n-1,m-1)!
   - Example: If you reach some far cell at distance 10, but destination is at distance 3,
     you'd return 10 (WRONG!) instead of 3

3. ❌ Not early terminating when destination is reached
   - Should check if (x,y) == (n-1, m-1) and immediately return dist
   - No need to explore further once destination found!

4. ❌ Using lastX, lastY variables that serve no purpose

CORRECT APPROACH: Early terminate when reaching destination!

================================================================================
EDGE CASES:
================================================================================
1. grid[0][0] = 1 → return -1 (start blocked)
2. grid[n-1][n-1] = 1 → return -1 (end blocked)
3. Single cell [[0]] → return 1
4. Single cell [[1]] → return -1
5. No path exists → return -1
6. Straight diagonal path → shortest = n

REAL-WORLD APPLICATIONS:
- Robot navigation on grid with obstacles
- Game pathfinding (chess king movement)
- Maze solving with diagonal moves
- Image processing - shortest path between pixels
"""

from collections import deque
from typing import List

class Solution:
    """
    BFS with Early Termination - CORRECT APPROACH
    TIME: O(n²) | SPACE: O(n²)
    """
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        # Edge cases
        if not grid or not grid[0]:
            return -1

        n = len(grid)

        # Check if start or end is blocked
        if grid[0][0] != 0 or grid[n-1][n-1] != 0:
            return -1

        # Special case: single cell
        if n == 1:
            return 1

        # 8 directions: up, down, left, right, and 4 diagonals
        # ALL 8 DIRECTIONS! Not 6!
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]

        # BFS: (row, col, distance)
        queue = deque([(0, 0, 1)])  # Start at (0,0) with distance 1
        visited = set()
        visited.add((0, 0))

        while queue:
            x, y, dist = queue.popleft()

            # EARLY TERMINATION: Found destination!
            # This is what your code was missing!
            if x == n-1 and y == n-1:
                return dist

            # Explore all 8 neighbors
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                # Check bounds, obstacle, and visited
                if (0 <= nx < n and 0 <= ny < n and
                    grid[nx][ny] == 0 and (nx, ny) not in visited):

                    queue.append((nx, ny, dist + 1))
                    visited.add((nx, ny))

        # Destination never reached
        return -1


# ============================================================================
# ALTERNATIVE: Without Early Termination (Store distances)
# ============================================================================
class SolutionNoEarlyTermination:
    """
    BFS without early termination - stores all distances
    TIME: O(n²) | SPACE: O(n²)

    Use this when you need distances to ALL cells, not just destination
    """
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        if not grid or grid[0][0] != 0:
            return -1

        n = len(grid)
        if grid[n-1][n-1] != 0:
            return -1

        if n == 1:
            return 1

        directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
        queue = deque([(0, 0, 1)])
        distances = {(0, 0): 1}  # Store distance to each cell

        while queue:
            x, y, dist = queue.popleft()

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if (0 <= nx < n and 0 <= ny < n and
                    grid[nx][ny] == 0 and (nx, ny) not in distances):

                    distances[(nx, ny)] = dist + 1
                    queue.append((nx, ny, dist + 1))

        # Return distance to destination, or -1 if unreachable
        return distances.get((n-1, n-1), -1)


"""
================================================================================
VISUAL EXAMPLE - Why maxD Approach Fails
================================================================================

Grid (3x3):
    0 0 1
    0 1 0
    1 0 0

Goal: Shortest path from (0,0) to (2,2)?

YOUR CODE's BFS Exploration:
Step 1: Start (0,0), dist=1
Step 2: Visit (0,1), dist=2
Step 3: Visit (1,0), dist=2
Step 4: Visit (2,1), dist=3 from (1,0)
Step 5: Visit (1,2), dist=4 from (2,1) ← maxD = 4!
Step 6: Visit (2,2), dist=5 from (1,2)

Your maxD tracking:
- maxD keeps getting updated to max distance seen
- When (1,2) is reached: maxD = 4
- Final check: (2,2) in visited? Yes → return maxD = 4

WRONG! The actual shortest distance to (2,2) is 5, but you'd return 4!

CORRECT APPROACH:
When you pop (2,2) from queue:
- Check if x==2 and y==2 → YES!
- Immediately return dist = 5 ✓

================================================================================
VISUAL EXAMPLE 2 - Step-by-Step BFS (Correct)
================================================================================

Grid (n=3):
    0 1 0
    0 0 0
    0 0 0

Goal: Shortest path from (0,0) to (2,2)

BFS Execution:
Queue: [(0,0,1)]
Visited: {(0,0)}

Process (0,0):
- Check if (0,0) == (2,2)? NO
- Explore 8 neighbors: only (1,0) and (1,1) valid
Queue: [(1,0,2), (1,1,2)]

Process (1,0):
- Check if (1,0) == (2,2)? NO
- Add (2,0), (2,1)
Queue: [(1,1,2), (2,0,3), (2,1,3)]

Process (1,1):
- Check if (1,1) == (2,2)? NO
- Add (0,2), (1,2), (2,2)
Queue: [(2,0,3), (2,1,3), (0,2,3), (1,2,3), (2,2,3)]

Process (2,0):
- Check if (2,0) == (2,2)? NO
Queue: [(2,1,3), (0,2,3), (1,2,3), (2,2,3)]

... keep processing ...

Process (2,2):
- Check if (2,2) == (2,2)? YES! ✓
- return dist = 3

ANSWER: 3
Path: (0,0) → (1,1) → (2,2) [diagonal moves]

================================================================================
WHY EARLY TERMINATION MATTERS:
================================================================================

Without early termination:
- BFS continues processing remaining cells in queue
- Wastes time exploring irrelevant paths
- Still O(n²) but with higher constant factor

With early termination:
- Stop immediately when destination found
- Best case: O(1) if start == destination
- Average case: Much faster in practice
- Worst case: Still O(n²) if destination is last cell processed

INTERVIEW TIP: Always mention early termination optimization for BFS shortest path!

================================================================================
FANG INTERVIEW TALKING POINTS:
================================================================================

1. "I recognize this as unweighted shortest path → BFS is optimal"

2. "Key difference from standard BFS: 8-directional movement (all adjacent + diagonals)"

3. "I'll early terminate when reaching destination for efficiency"

4. "Critical: Use 8 directions, not 4 or 6!"

5. "Edge cases: blocked start/end, single cell, no path exists"

6. "Time O(n²), Space O(n²) - visit each cell once, queue can hold O(n²) cells"

7. "Distance is 1-indexed - start cell counts as 1, not 0 (path length includes start)"

8. "Common mistake: tracking max distance to ANY cell instead of distance to destination"

SUMMARY OF FIXES FROM YOUR CODE:
1. Added missing 2 diagonal directions
2. Removed maxD tracking (wrong approach)
3. Added early termination when reaching (n-1, n-1)
4. Removed unused lastX, lastY variables
5. Simplified to return dist directly when destination found
"""
