"""
================================================================================
PATTERN: Minimum Effort Path - Dijkstra Variant (Min-Max Path)
================================================================================

PROBLEM:
Find path from top-left to bottom-right where the maximum absolute difference
between consecutive cells is minimized.

KEY INSIGHT - MODIFIED DIJKSTRA:
Instead of minimizing SUM of edge weights (standard Dijkstra),
we minimize the MAXIMUM edge weight along the path.

Edge weight = |height[cell1] - height[cell2]|
Path effort = max(all edge weights in path)
Goal: Find path with minimum effort

DIFFERENCE FROM STANDARD DIJKSTRA:
Standard: distance[v] = distance[u] + weight(u,v)  → SUM
This problem: effort[v] = max(effort[u], weight(u,v))  → MAX

ALGORITHM:
1. Use priority queue (min-heap) to always process cell with smallest effort
2. For each cell, relax neighbors: effort = max(current_effort, edge_weight)
3. Early terminate when reaching destination
4. Greedy: Once destination popped from PQ, we have optimal answer

TIME COMPLEXITY: O(n*m * log(n*m))
- Each cell added to PQ at most once: O(n*m) insertions
- Each PQ operation: O(log(n*m))
- Total: O(n*m * log(n*m))

SPACE COMPLEXITY: O(n*m)
- Distance matrix: O(n*m)
- Priority queue: O(n*m) worst case
"""

import heapq
from typing import List

def minimumEffortPath(heights: List[List[int]]) -> int:
    if not heights or not heights[0]:
        return 0

    n, m = len(heights), len(heights[0])
    if n == 1 and m == 1:
        return 0

    # Distance = minimum effort to reach each cell
    effort = [[float('inf')] * m for _ in range(n)]
    effort[0][0] = 0

    # Priority queue: (effort, row, col)
    pq = [(0, 0, 0)]
    directions = [(-1,0), (1,0), (0,-1), (0,1)]

    while pq:
        curr_effort, x, y = heapq.heappop(pq)

        # Early termination - found destination
        if x == n-1 and y == m-1:
            return curr_effort

        # Skip stale entries
        if curr_effort > effort[x][y]:
            continue

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < n and 0 <= ny < m:
                # Edge weight = absolute difference in heights
                edge_weight = abs(heights[x][y] - heights[nx][ny])

                # New effort = max effort along this path
                new_effort = max(curr_effort, edge_weight)

                # Relax if found better path
                if new_effort < effort[nx][ny]:
                    effort[nx][ny] = new_effort
                    heapq.heappush(pq, (new_effort, nx, ny))

    return effort[n-1][m-1]


"""
EXAMPLE TRACE:
Grid: [[1,2,2],
       [3,8,2],
       [5,3,5]]

Goal: (0,0) → (2,2) with minimum maximum difference

Step-by-step:
1. Start (0,0), effort=0
2. Process neighbors:
   - (0,1): |1-2|=1, effort=max(0,1)=1
   - (1,0): |1-3|=2, effort=max(0,2)=2
3. Pop (0,1) with effort=1:
   - (0,2): |2-2|=0, effort=max(1,0)=1
   - (1,1): |2-8|=6, effort=max(1,6)=6
4. Pop (0,2) with effort=1:
   - (1,2): |2-2|=0, effort=max(1,0)=1
5. Pop (1,2) with effort=1:
   - (2,2): |2-5|=3, effort=max(1,3)=3

Answer: 3 (path: (0,0)→(0,1)→(0,2)→(1,2)→(2,2))

FANG INTERVIEW POINTS:
1. "This is Dijkstra variant - instead of sum, we track maximum edge weight"
2. "Use min-heap to greedily process lowest effort paths first"
3. "Early terminate when destination popped from PQ"
4. "Time: O(nm log nm), Space: O(nm)"
"""
