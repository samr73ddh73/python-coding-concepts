"""
TOPOLOGICAL SORT - DFS Approach

PURPOSE: Order nodes such that if u→v exists, u comes before v
WORKS ONLY ON: DAGs (Directed Acyclic Graphs)

TIME COMPLEXITY: O(V + E)
  - Visit each vertex once: O(V)
  - Process each edge once: O(E)
  - Total: O(V + E)

SPACE COMPLEXITY: O(V)
  - visited set: O(V)
  - recursion stack (worst case chain): O(V)
  - result stack: O(V)

WHY POST-ORDER DFS?
====================
Key insight: Add node to stack AFTER exploring all neighbors
- When we backtrack from a node, it means we've explored all its descendants
- At that point, the node has "lower priority" (comes earlier in topo order)
- Reversing the stack gives us the topological order

Example:
    0 → 1 → 2
    └→ 3

Post-order DFS traversal (when backtracking):
  2 (leaf, backtrack immediately)
  1 (after exploring 2)
  3 (leaf, backtrack immediately)
  0 (after exploring all)

Stack: [2, 1, 3, 0]
Reverse: [0, 3, 1, 2]

Verify: 0 comes before 1,3; 1 comes before 2; 3 comes before nothing ✓

WHY REVERSE?
=============
We add nodes during BACKTRACKING (post-order):
- Deeper nodes (leaves) get added first
- Root gets added last

So stack is in reverse topological order.
Reverse it to get actual topological order.
"""

from collections import deque

def topoSort(graph, V):
    """
    Topological sort using DFS post-order traversal.

    Time: O(V + E)
    Space: O(V)
    """
    visited = set()
    stack = []

    # Visit all nodes (handles disconnected components)
    for i in range(V):
        if i not in visited:
            dfs(graph, i, visited, stack)

    # Reverse because we added in post-order (backwards)
    return stack[::-1]

def dfs(graph, start, visited, stack):
    """
    DFS post-order: add to stack AFTER processing neighbors.
    This ensures dependencies come first.
    """
    visited.add(start)

    # Explore all neighbors first
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited, stack)

    # CRITICAL: Add current node AFTER exploring all neighbors (post-order)
    # This ensures topological ordering when reversed
    stack.append(start)

def main():
    V = 6
    graph ={
        0: [],
        1: [2, 5],
        2: [3],
        3: [4],
        4: [],
        5: [6],
        6: [7,8],
        7: [],
        8: []
    }

    print(topoSort(graph, V))

if __name__ == '__main__':
    main()
    
    