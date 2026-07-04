"""
Unique Paths II

LeetCode 63: https://leetcode.com/problems/unique-paths-ii/description/

Problem:
--------
You are given an m x n integer array obstacleGrid. There is a robot starting at the top-left
corner (grid[0][0]), and it tries to move to the bottom-right corner (grid[m-1][n-1]).

The robot can only move either down or right at any point in time.

An obstacle and empty space are marked as 1 or 0 respectively. A path cannot include any obstacle.

Return the number of possible unique paths that the robot can take to reach the bottom-right corner.

Examples:
---------
Example 1:
    Input: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
    Output: 2
    Explanation: Two paths (avoiding the obstacle at middle)

Example 2:
    Input: obstacleGrid = [[0,1],[0,0]]
    Output: 1
    Explanation: Only one path due to obstacle at (0,1)

Why This is DP on Grids (Not BFS):
-----------------------------------
- Problem asks: "Count the number of unique paths"
- Multiple paths can reach the same cell
- We need to COMBINE counts from all paths, not find just one
- BFS with visited: Would only find ONE path
- BFS without visited: Would cause infinite loops
- DP with memoization: Counts ALL paths by combining subproblems

State Definition:
-----------------
dp(i, j) = "number of ways to reach cell (i, j) from (0, 0)"

Recurrence:
-----------
dp(i, j) = dp(i+1, j) + dp(i, j+1)
         = (ways from going down) + (ways from going right)

Base Cases:
-----------
1. Out of bounds: return 0
2. Hit obstacle: return 0
3. Reached destination: return 1

Time Complexity: O(m × n) - each cell computed once
Space Complexity: O(m × n) - memoization table + recursion depth
"""

from typing import List

class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        """
        Top-Down DP (Memoization) approach.

        Why top-down for this problem?
        - Natural recursive structure (move right or down)
        - Handles obstacles easily (return 0 immediately)
        - Memoization prevents recomputation of overlapping subproblems
        - Clear base cases
        """

        # Edge case: start position is obstacle
        if not obstacleGrid or obstacleGrid[0][0] == 1:
            return 0

        memo = {}
        rows, cols = len(obstacleGrid), len(obstacleGrid[0])

        def dp(i, j):
            """
            Returns the number of ways to reach (i, j) from (0, 0).

            Args:
                i: row index
                j: column index

            Returns:
                Number of unique paths from (0, 0) to (i, j)
            """

            # Base case 1: Out of bounds - can't reach destination from here
            if i >= rows or j >= cols:
                return 0

            # Base case 2: Obstacle - blocks all paths through this cell
            if obstacleGrid[i][j] == 1:
                return 0

            # Base case 3: Reached destination - one way to be here
            if i == rows - 1 and j == cols - 1:
                return 1

            # Check memoization: if already computed, return cached result
            if (i, j) in memo:
                return memo[(i, j)]

            # Recurrence: sum paths from moving down + paths from moving right
            # We can only reach (i, j) from (i-1, j) or (i, j-1)
            # So ways to reach (i, j) = ways from top + ways from left
            # But we're computing top-down, so we look at where we can go FROM (i, j)
            down_paths = dp(i + 1, j)      # paths by going down
            right_paths = dp(i, j + 1)     # paths by going right

            result = down_paths + right_paths
            memo[(i, j)] = result
            return result

        return dp(0, 0)


# ============================================================================
# ALTERNATIVE: Bottom-Up DP (Iterative)
# ============================================================================

class SolutionBottomUp:
    """
    Bottom-Up DP (Iterative) approach.

    Advantages:
    - No recursion overhead
    - Faster in practice
    - Systematic iteration (left→right, top→bottom)

    Disadvantages:
    - Must handle edges explicitly
    - More verbose
    """

    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        if not obstacleGrid or obstacleGrid[0][0] == 1:
            return 0

        rows, cols = len(obstacleGrid), len(obstacleGrid[0])

        # dp[i][j] = number of ways to reach (i, j)
        dp = [[0] * cols for _ in range(rows)]

        # Base case: one way to be at start
        dp[0][0] = 1

        # Fill first row (can only come from left)
        for j in range(1, cols):
            if obstacleGrid[0][j] != 1:
                dp[0][j] = dp[0][j - 1]
            else:
                dp[0][j] = 0  # obstacle blocks

        # Fill first column (can only come from top)
        for i in range(1, rows):
            if obstacleGrid[i][0] != 1:
                dp[i][0] = dp[i - 1][0]
            else:
                dp[i][0] = 0  # obstacle blocks

        # Fill rest of table (can come from top or left)
        for i in range(1, rows):
            for j in range(1, cols):
                if obstacleGrid[i][j] == 1:
                    dp[i][j] = 0  # obstacle blocks all paths
                else:
                    dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

        return dp[rows - 1][cols - 1]


# ============================================================================
# TEST CASES
# ============================================================================

if __name__ == "__main__":
    sol = Solution()
    sol_bu = SolutionBottomUp()

    # Test case 1: Simple with obstacle
    grid1 = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    print(f"Test 1 - Top-Down: {sol.uniquePathsWithObstacles(grid1)}")  # Expected: 2
    print(f"Test 1 - Bottom-Up: {sol_bu.uniquePathsWithObstacles(grid1)}")  # Expected: 2

    # Test case 2: Obstacle at top-right
    grid2 = [[0, 1], [0, 0]]
    print(f"Test 2 - Top-Down: {sol.uniquePathsWithObstacles(grid2)}")  # Expected: 1
    print(f"Test 2 - Bottom-Up: {sol_bu.uniquePathsWithObstacles(grid2)}")  # Expected: 1

    # Test case 3: Obstacle at start
    grid3 = [[1, 0], [0, 0]]
    print(f"Test 3 - Top-Down: {sol.uniquePathsWithObstacles(grid3)}")  # Expected: 0
    print(f"Test 3 - Bottom-Up: {sol_bu.uniquePathsWithObstacles(grid3)}")  # Expected: 0

    # Test case 4: No obstacles
    grid4 = [[0, 0], [0, 0]]
    print(f"Test 4 - Top-Down: {sol.uniquePathsWithObstacles(grid4)}")  # Expected: 2
    print(f"Test 4 - Bottom-Up: {sol_bu.uniquePathsWithObstacles(grid4)}")  # Expected: 2

    # Test case 5: Single cell
    grid5 = [[0]]
    print(f"Test 5 - Top-Down: {sol.uniquePathsWithObstacles(grid5)}")  # Expected: 1
    print(f"Test 5 - Bottom-Up: {sol_bu.uniquePathsWithObstacles(grid5)}")  # Expected: 1


"""
Key Insights:
=============

1. WHY DP, NOT BFS?
   - Counting paths requires summing ALL paths
   - BFS with visited: Only finds ONE path
   - BFS without visited: Infinite loop
   - DP with memoization: Counts all by combining subproblems

2. STATE DEFINITION
   dp(i, j) = ways to reach (i, j) from (0, 0)

3. RECURRENCE
   dp(i, j) = dp(i+1, j) + dp(i, j+1)
   = (paths going down) + (paths going right)

4. BASE CASES
   - Out of bounds: 0
   - Obstacle: 0
   - Destination: 1

5. MEMOIZATION vs VISITED
   - BFS visited: Prevents revisits (for finding ONE solution)
   - DP memo: Prevents recomputation (for combining solutions)
   - These serve different purposes!

6. COMPLEXITY
   - Time: O(m × n) - each cell computed once
   - Space: O(m × n) - memo table + recursion depth
"""
