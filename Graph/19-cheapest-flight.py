"""
================================================================================
PATTERN: Cheapest Flights with K Stops - Modified Dijkstra
================================================================================

PROBLEM:
Find cheapest price from src to dst with at most K stops.

KEY INSIGHT - WHY STANDARD DIJKSTRA FAILS:
Standard Dijkstra: Once we find cheapest path to node X, we're done with X
This problem: A MORE EXPENSIVE path to X with FEWER stops might lead to cheaper final answer!

Example:
- Reach node 1 via: 0→5→1 (cost 101, stops 1)
- Reach node 1 via: 0→7→8→9→1 (cost 4, stops 3)
- First path is expensive but can explore further (fewer stops used)
- Second path is cheap but might exceed stop limit!

WRONG: if price < distance[node]: skip
RIGHT: Track (node, stops) as separate states

TIME: O(E * K * log(E*K)) where E=edges, K=stops
SPACE: O(n*K) for tracking (node, stops) states
"""

import heapq
from collections import defaultdict
from typing import List

def findCheapestPrice(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
    graph = defaultdict(list)
    for u, v, price in flights:
        graph[u].append((v, price))

    # Priority queue: (cost, node, stops)
    pq = [(0, src, 0)]

    # Track min cost to reach (node, stops) state
    # Key insight: same node with different stops = different states!
    visited = {}  # (node, stops) -> min_cost

    while pq:
        cost, node, stops = heapq.heappop(pq)

        # Found destination
        if node == dst:
            return cost

        # Exceeded stop limit
        if stops > k:
            continue

        # Skip if we've processed this (node, stops) state with better cost
        if (node, stops) in visited:
            continue
        visited[(node, stops)] = cost

        # Explore neighbors
        for neighbor, price in graph[node]:
            new_cost = cost + price
            new_stops = stops + 1

            # Only explore if not visited OR found better cost for this state
            if (neighbor, new_stops) not in visited:
                heapq.heappush(pq, (new_cost, neighbor, new_stops))

    return -1

"""
WHY YOUR CODE FAILED - DETAILED TRACE:

Your buggy line 26: if price+wt < distance[neighbor]:

This skips revisiting nodes, but that's WRONG for stop-constrained problems!

Trace with your input (src=0, dst=2, k=4):

Step 1: Process (0, cost=0, stops=0)
  - Push (5, cost=1, stops=1)
  - Push (7, cost=1, stops=1)
  - distance[5]=1, distance[7]=1

Step 2: Process (5, cost=1, stops=1)
  - Neighbor 1: cost=1+100=101
  - 101 < distance[1]=inf ✓
  - Push (1, cost=101, stops=2)
  - distance[1]=101

Step 3: Process (7, cost=1, stops=1)
  - Neighbor 8: cost=1+1=2
  - Push (8, cost=2, stops=2)

Step 4: Process (8, cost=2, stops=2)
  - Neighbor 9: Push (9, cost=3, stops=3)

Step 5: Process (9, cost=3, stops=3)
  - Neighbor 1: cost=3+1=4
  - Check: 4 < distance[1]=101 ✓
  - Push (1, cost=4, stops=4)
  - distance[1]=4 ← Updated!

Step 6: Process (1, cost=4, stops=4)
  - Neighbor 10: cost=4+1=5, stops=5 > k=4 ✗ SKIP!
  - Neighbor 2: cost=4+100=104, stops=5 > k=4 ✗ SKIP!

Step 7: Process (1, cost=101, stops=2) [stale from Step 2]
  - Check: 101 > distance[1]=4, SKIP! ← BUG!
  - This path COULD have reached node 2 in stops=2+2=4!

Result: distance[2]=inf → return -1 or wrong value

CORRECT ANSWER: 0→3→4→1→10→2 = 3+3+3+1+1 = 11 with 4 stops ✓

FIXED APPROACH:
Track (node, stops) separately - visiting node 1 with stops=2 is DIFFERENT
from visiting node 1 with stops=4, even if cost is higher!
"""

def main():
    flights = [[0,3,3],[3,4,3],[4,1,3],[0,5,1],[5,1,100],[0,6,2],[6,1,100],
               [0,7,1],[7,8,1],[8,9,1],[9,1,1],[1,10,1],[10,2,1],[1,2,100]]
    n = 11
    result = findCheapestPrice(n, flights, 0, 2, 4)
    print(f"Result: {result}")  # Expected: 11
    # Path: 0→3(3) → 4(3) → 1(3) → 10(1) → 2(1) = 11, stops=4 ✓

if __name__ == '__main__':
    main()


"""
FANG INTERVIEW POINTS:

1. "This is modified Dijkstra with stop constraint - can't use standard distance pruning"

2. "Key insight: Track (node, stops) as distinct states, not just node"

3. "A more expensive path with fewer stops might unlock cheaper final routes"

4. "Use visited[(node, stops)] to avoid reprocessing same state"

5. "Early termination: Return when destination popped (guaranteed optimal due to min-heap)"

6. "Time: O(E*K*log(E*K)), Space: O(n*K) for state tracking"
"""