"""
================================================================================
PATTERN: Dijkstra's Shortest Path Algorithm using Priority Queue (Min-Heap)
================================================================================

PROBLEM:
Given a weighted graph with NON-NEGATIVE edge weights, find the shortest path
from a source node to all other nodes.

KEY INSIGHT - GREEDY + PRIORITY QUEUE:
- Always process the node with smallest known distance first (greedy)
- Use priority queue (min-heap) to efficiently get minimum distance node
- Once a node is processed, its shortest distance is FINAL (optimal substructure)

WHY PRIORITY QUEUE?
Without PQ: O(V�) - Linear search for minimum distance node each time
With PQ: O((V+E) log V) - Efficient extraction of minimum

ALGORITHM:
1. Initialize distances: source = 0, all others = infinity
2. Add source to priority queue with distance 0
3. While PQ not empty:
   a. Extract node with minimum distance (greedy choice)
   b. If already processed (visited), skip
   c. Mark as visited (distance is now final)
   d. For each neighbor, try to relax edge:
      - If new_dist < current_dist, update distance and add to PQ
4. Return distance array

================================================================================
PRIORITY QUEUE IN PYTHON: heapq module
================================================================================

Python's heapq implements a MIN-HEAP (smallest element has highest priority)

IMPORTANT OPERATIONS:
- heappush(heap, item): Add item - O(log n)
- heappop(heap): Remove and return smallest - O(log n)
- heap[0]: Peek at smallest - O(1)
- heapify(list): Convert list to heap in-place - O(n)

HEAP STRUCTURE FOR DIJKSTRA:
Store tuples: (distance, node)
- Python compares tuples lexicographically: (1, 'a') < (2, 'b')
- First element (distance) determines priority
- Heap automatically maintains min-distance at top

EXAMPLE:
import heapq
pq = []
heapq.heappush(pq, (5, 'A'))  # (distance, node)
heapq.heappush(pq, (2, 'B'))
heapq.heappush(pq, (8, 'C'))
heapq.heappop(pq)  # Returns (2, 'B') - smallest distance

================================================================================
TIME COMPLEXITY: O((V + E) log V)
================================================================================

DETAILED BREAKDOWN:
1. Initialization: O(V) - Set all distances to infinity
2. Main loop: Each vertex added to PQ at most once � O(V) insertions
3. Heap operations:
   - Each insert: O(log V)
   - Each extract-min: O(log V)
   - Total vertices: V operations � O(V log V)
4. Edge relaxations:
   - Each edge relaxed at most once
   - Each relaxation may add to PQ: O(log V)
   - Total edges: E operations � O(E log V)

TOTAL: O(V log V + E log V) = O((V + E) log V)

For dense graphs (E H V�): O(V� log V)
For sparse graphs (E H V): O(V log V)

SPACE COMPLEXITY: O(V)
- Distance array: O(V)
- Priority queue: O(V) in worst case (all nodes in PQ)
- Visited set: O(V)
- Total: O(V)

================================================================================
COMPARISON WITH OTHER ALGORITHMS:
================================================================================

WHEN TO USE DIJKSTRA:
 Non-negative edge weights (REQUIRED!)
 Need single-source shortest path
 Graph is sparse (E << V�) - PQ version is better
 Real-time applications (GPS, routing)

L DON'T USE when:
- Graph has negative weights (use Bellman-Ford)
- Graph is a DAG (use topological sort - faster!)
- All edges have weight 1 (use BFS - simpler!)

================================================================================
WHY NO NEGATIVE WEIGHTS?
================================================================================

Dijkstra's greedy assumption: Once a node is visited, its distance is FINAL.

Counter-example with negative weight:
  A --1--> B --(-3)--> C
  A -------2----------> C

Dijkstra would:
1. Visit A (dist = 0)
2. Visit B (dist = 1) - marks B as final 
3. Visit C via direct path (dist = 2) - marks C as final 
4. NEVER revisits C via B�C path (dist = -2) 

Correct shortest path: A�B�C = 1 + (-3) = -2
Dijkstra's answer: A�C = 2 L

The greedy choice fails because negative weights can make longer paths shorter!

================================================================================
PYTHON INTERNALS: heapq
================================================================================

- heapq uses a MIN-HEAP (not max-heap)
- Implemented as a binary heap in a list
- Parent at index i, children at 2i+1 and 2i+2
- Heap property: heap[i] <= heap[2i+1] and heap[i] <= heap[2i+2]

TRICK for MAX-HEAP:
- Store negative values: heappush(pq, -value)
- Extract and negate: -heappop(pq)

HANDLING DUPLICATES:
- Same node can appear multiple times in PQ with different distances
- Always process the smallest distance first
- Use visited set to skip already-processed nodes
- This is OK! Extra entries are harmless (just skipped)

EDGE CASES:
1. Source node � distance = 0
2. Unreachable nodes � distance = infinity
3. Self-loops with positive weight � ignored (already have dist 0)
4. Multiple edges between same nodes � take minimum weight
5. Disconnected graph � some nodes stay at infinity
"""

import heapq
from typing import List, Dict, Tuple


def dijkstra(graph: Dict[int, List[Tuple[int, int]]], start: int, V: int) -> List[float]:
    # Step 1: Initialize distances - O(V)
    distance = [float('inf')] * V
    distance[start] = 0

    # Step 2: Initialize priority queue (min-heap) - O(1)
    # Format: (distance, node)
    pq = [(0, start)]  # Start with source at distance 0

    # Step 3: Track visited nodes to avoid reprocessing
    visited = set()

    # Step 4: Process nodes in order of increasing distance - O((V+E) log V)
    while pq:
        # Extract node with minimum distance (greedy choice) - O(log V)
        curr_dist, node = heapq.heappop(pq)

        # Skip if already processed (may have duplicates in PQ)
        if node in visited:
            continue

        # Mark as visited - distance is now FINAL
        visited.add(node)

        # Optimization: if curr_dist > distance[node], skip (stale entry)
        if curr_dist > distance[node]:
            continue

        # Step 5: Relax all edges from current node - O(degree(node))
        if node in graph:
            for neighbor, weight in graph[node]:
                # Calculate new distance via current node
                new_dist = distance[node] + weight

                # Edge relaxation: update if found shorter path
                if new_dist < distance[neighbor]:
                    distance[neighbor] = new_dist
                    # Add to PQ with new distance - O(log V)
                    heapq.heappush(pq, (new_dist, neighbor))

    return distance


def dijkstra_with_path(graph: Dict[int, List[Tuple[int, int]]], start: int, V: int) -> Tuple[List[float], Dict[int, int]]:
    """
    Dijkstra's algorithm that also returns the shortest path tree

    Returns:
        - distance: List of shortest distances
        - parent: Dict mapping each node to its predecessor in shortest path

    To reconstruct path from start to node X:
        path = []
        current = X
        while current != start:
            path.append(current)
            current = parent[current]
        path.append(start)
        path.reverse()
    """
    distance = [float('inf')] * V
    distance[start] = 0
    parent = {start: None}  # Track predecessors for path reconstruction

    pq = [(0, start)]
    visited = set()

    while pq:
        curr_dist, node = heapq.heappop(pq)

        if node in visited:
            continue

        visited.add(node)

        if node in graph:
            for neighbor, weight in graph[node]:
                new_dist = distance[node] + weight

                if new_dist < distance[neighbor]:
                    distance[neighbor] = new_dist
                    parent[neighbor] = node  # Track where we came from
                    heapq.heappush(pq, (new_dist, neighbor))

    return distance, parent


def reconstruct_path(parent: Dict[int, int], start: int, end: int) -> List[int]:
    """
    Reconstruct shortest path from start to end using parent dict

    Returns:
        List of nodes in path from start to end
        Empty list if no path exists
    """
    if end not in parent:
        return []  # No path exists

    path = []
    current = end

    while current is not None:
        path.append(current)
        current = parent.get(current)

    path.reverse()
    return path if path[0] == start else []


# ============================================================================
# EXAMPLE USAGE
# ============================================================================
def main():
    # Example graph:
    #     1 --2-- 2
    #    /|      /|
    #   4 |1    1 |3
    #  /  |  /    |
    # 0   | /     4
    #  \  |/     /
    #   2 3 --1-/

    V = 5  # Nodes: 0, 1, 2, 3, 4
    graph = {
        0: [(1, 4), (3, 2)],      # 0 connects to 1 (weight 4), 3 (weight 2)
        1: [(0, 4), (2, 2), (3, 1)],  # 1 connects to 0, 2, 3
        2: [(1, 2), (3, 1), (4, 3)],  # 2 connects to 1, 3, 4
        3: [(0, 2), (1, 1), (2, 1), (4, 1)],  # 3 is central hub
        4: [(2, 3), (3, 1)]       # 4 connects to 2, 3
    }

    start = 0

    # Find shortest distances
    distances = dijkstra(graph, start, V)

    print(f"Shortest distances from node {start}:")
    for node, dist in enumerate(distances):
        print(f"  Node {node}: {dist}")

    print()

    # Find shortest paths
    distances, parent = dijkstra_with_path(graph, start, V)

    print("Shortest paths from node 0:")
    for node in range(V):
        if node != start:
            path = reconstruct_path(parent, start, node)
            if path:
                print(f"  0 � {node}: {' � '.join(map(str, path))} (distance: {distances[node]})")
            else:
                print(f"  0 � {node}: No path exists")


if __name__ == '__main__':
    main()


"""
================================================================================
VISUAL EXAMPLE - Step-by-Step Trace
================================================================================

Graph:
      1 --2-- 2
     /|      /|
    4 |1    1 |3
   /  |  /    |
  0   | /     4
   \  |/     /
    2 3 --1-/

Starting from node 0:

INITIALIZATION:
distance = [0, inf, inf, inf, inf]
PQ = [(0, 0)]
visited = {}

ITERATION 1: Process node 0 (dist=0)
- Visit node 0, mark visited
- Relax edges: 0�1(4), 0�3(2)
- Update: distance[1]=4, distance[3]=2
- PQ = [(2, 3), (4, 1)]
- visited = {0}
- distance = [0, 4, inf, 2, inf]

ITERATION 2: Process node 3 (dist=2)
- Visit node 3, mark visited
- Relax edges: 3�0(2), 3�1(1), 3�2(1), 3�4(1)
- 3�0: 2+2=4 NOT < 0, skip
- 3�1: 2+1=3 < 4, update distance[1]=3
- 3�2: 2+1=3 < inf, update distance[2]=3
- 3�4: 2+1=3 < inf, update distance[4]=3
- PQ = [(3, 1), (3, 2), (3, 4), (4, 1)]
- visited = {0, 3}
- distance = [0, 3, 3, 2, 3]

ITERATION 3: Process node 1 (dist=3)
- Visit node 1, mark visited
- Relax edges: 1�0(4), 1�2(2), 1�3(1)
- All new distances are NOT better, no updates
- PQ = [(3, 2), (3, 4), (4, 1)]
- visited = {0, 3, 1}
- distance = [0, 3, 3, 2, 3]

ITERATION 4: Process node 2 (dist=3)
- Visit node 2, mark visited
- Relax edges: 2�1(2), 2�3(1), 2�4(3)
- All new distances are NOT better, no updates
- PQ = [(3, 4), (4, 1)]
- visited = {0, 3, 1, 2}
- distance = [0, 3, 3, 2, 3]

ITERATION 5: Process node 4 (dist=3)
- Visit node 4, mark visited
- Relax edges: 4�2(3), 4�3(1)
- All new distances are NOT better, no updates
- PQ = [(4, 1)] (stale entry)
- visited = {0, 3, 1, 2, 4}
- distance = [0, 3, 3, 2, 3]

ITERATION 6: Process node 1 (dist=4) - STALE ENTRY
- Node 1 already visited, skip
- PQ = []

FINAL RESULT:
distance = [0, 3, 3, 2, 3]

Shortest paths from node 0:
- 0�0: 0 (path: 0)
- 0�1: 3 (path: 0�3�1)
- 0�2: 3 (path: 0�3�2)
- 0�3: 2 (path: 0�3)
- 0�4: 3 (path: 0�3�4)

================================================================================
FANG INTERVIEW TALKING POINTS
================================================================================

1. "I'll use Dijkstra's algorithm with a min-heap priority queue for O((V+E)logV)"

2. "Key insight: Always process the node with smallest known distance (greedy).
   Once processed, that distance is final due to non-negative weights"

3. "I'm using Python's heapq module which implements a min-heap. I'll store
   (distance, node) tuples so the heap prioritizes by distance"

4. "Important: same node can appear multiple times in PQ with different distances.
   I'll use a visited set to skip already-processed nodes"

5. "Time: O((V+E)logV) - Each vertex/edge processed once, heap ops are O(logV)"
   "Space: O(V) - distance array, PQ, and visited set"

6. "Edge cases: unreachable nodes stay at infinity, disconnected components handled"

7. "Limitation: Only works with non-negative weights. For negative weights,
   need Bellman-Ford O(VE). For DAGs, topological sort is faster O(V+E)"

COMMON MISTAKES TO AVOID:
- Forgetting to check if node already visited (causes reprocessing)
- Using max-heap instead of min-heap
- Not handling negative weights (Dijkstra breaks!)
- Forgetting tuple format: (distance, node) not (node, distance)
- Not initializing source distance to 0

OPTIMIZATION TRICKS:
- Early termination: if target found, can stop
- Bidirectional search: search from both ends simultaneously
- A* algorithm: Dijkstra + heuristic for goal-directed search
"""
