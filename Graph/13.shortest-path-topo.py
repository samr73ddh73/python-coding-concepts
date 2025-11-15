"""
================================================================================
PATTERN: Shortest Path in DAG using Topological Sort
================================================================================

PROBLEM:
Given a weighted Directed Acyclic Graph (DAG), find the shortest path from a
source node to all other nodes.

KEY INSIGHT - WHY TOPOLOGICAL SORT?
Traditional shortest path algorithms:
- Dijkstra: O((V+E) log V) - Uses priority queue, doesn't handle negative weights
- Bellman-Ford: O(V×E) - Handles negative weights but slower

TOPOLOGICAL SORT APPROACH: O(V + E) - FASTEST for DAGs!
- Process nodes in topological order (dependencies first)
- Each node processed exactly ONCE (no revisiting needed)
- Works with NEGATIVE weights (unlike Dijkstra)
- Simpler than both Dijkstra and Bellman-Ford

WHY IT WORKS:
1. DAG has no cycles → has valid topological ordering
2. Process nodes in dependency order: if u→v edge exists, process u before v
3. When we process node u, we've already found shortest path to u
4. Can safely relax all edges from u (won't need to revisit u)
5. Guaranteed optimal since we process in correct dependency order

ALGORITHM:
1. Compute topological sort of reachable nodes from source
2. Initialize distances: source = 0, all others = infinity
3. Process nodes in topological order:
   - For each neighbor, relax edge: dist[v] = min(dist[v], dist[u] + weight(u,v))
4. Return distance array

================================================================================
TIME COMPLEXITY ANALYSIS: O(V + E)
================================================================================

STEP 1: Topological Sort via DFS
- Visit each node once: O(V)
- Explore each edge once: O(E)
- Reversing stack: O(V)
- Total: O(V + E)

STEP 2: Edge Relaxation
- Iterate through topological order: O(V)
- For each node, check all outgoing edges
- Total edges checked across all nodes: O(E)
- Total: O(V + E)

OVERALL: O(V + E) + O(V + E) = O(V + E)

This is OPTIMAL for shortest path in DAG!

COMPARISON WITH OTHER ALGORITHMS:
┌─────────────────┬──────────────────┬──────────────┬────────────────┐
│   Algorithm     │  Time Complexity │ Neg Weights? │   Graph Type   │
├─────────────────┼──────────────────┼──────────────┼────────────────┤
│ Topo Sort (DAG) │  O(V + E)        │     ✅       │   DAG only     │
│ Dijkstra        │  O((V+E) log V)  │     ❌       │   Any graph    │
│ Bellman-Ford    │  O(V × E)        │     ✅       │   Any graph    │
│ BFS (unweighted)│  O(V + E)        │     N/A      │   Unweighted   │
└─────────────────┴──────────────────┴──────────────┴────────────────┘

SPACE COMPLEXITY: O(V)
- Distance array: O(V)
- Visited set: O(V)
- Topological sort stack: O(V)
- Recursion stack (DFS): O(V) in worst case (linear graph)
- Total: O(V)

================================================================================
WHEN TO USE THIS ALGORITHM:
================================================================================

✅ USE when:
1. Graph is a DAG (directed acyclic graph)
2. Need shortest path from single source
3. Graph may have negative edge weights
4. Need optimal O(V+E) performance

❌ DON'T USE when:
1. Graph has cycles (use Dijkstra or Bellman-Ford)
2. Graph is undirected (convert to directed or use Dijkstra)
3. Need all-pairs shortest path (use Floyd-Warshall)

REAL-WORLD APPLICATIONS:
- Project scheduling (PERT/CPM) - critical path
- Course prerequisite planning
- Build dependency resolution (Makefiles)
- Task scheduling with dependencies
- Version control merge ordering

================================================================================
EDGE CASES:
================================================================================
1. Source unreachable from some nodes → those stay at infinity ✓
2. Single node → distance = [0]
3. No edges from source → all others at infinity
4. Negative weights → works correctly (unlike Dijkstra)
5. Graph is just a linear chain → O(V+E) = O(V)

PYTHON INTERNALS:
- float('inf') for unreachable nodes
- Stack reversal [::-1] is O(n)
- Set for visited: O(1) lookup
"""

def findShortestPath(graph, start, V):
    # Step 1: Initialize distances - O(V)
    distance = [float('inf') for _ in range(V)]
    visited = set()
    distance[start] = 0

    # Step 2: Get topological sort of reachable nodes - O(V + E)
    topoSort = topologicalSort(graph, start, visited, [])

    # Step 3: Process nodes in topological order - O(V + E)
    # Relax edges: update distances to neighbors
    for node in topoSort:
        # Only process if node is reachable (distance != infinity)
        if distance[node] != float('inf'):
            for neighbor, wt in graph[node]:
                # Edge relaxation: if we found a shorter path, update it
                if distance[neighbor] > distance[node] + wt:
                    distance[neighbor] = distance[node] + wt

    return distance


def topologicalSort(graph, start, visited, stack):
    visited.add(start)

    # Visit all unvisited neighbors (DFS)
    for neighbor, wt in graph[start]:
        if neighbor not in visited:
            topologicalSort(graph, neighbor, visited, stack)

    # Add current node AFTER visiting all children (post-order)
    stack.append(start)

    # Reverse to get correct topological order
    # (nodes with no dependencies first)
    return stack[::-1]

def main():
    V = 6
    graph ={
        0: [(1,1)],
        1: [(2,1)],
        2: [(3,5), (4,8)],
        3: [(4,2)],
        4: [(5,1)],
        5: []
    }

    print(findShortestPath(graph, 0, V))

if __name__ == '__main__':
    main()


"""
================================================================================
VISUAL EXAMPLE - Step-by-Step Trace
================================================================================

Graph:
    0 --1--> 1 --1--> 2 --5--> 3 --2--> 4 --1--> 5
                       |              ^
                       +-----8--------+

Adjacency List:
0: [(1,1)]
1: [(2,1)]
2: [(3,5), (4,8)]
3: [(4,2)]
4: [(5,1)]
5: []

STEP 1: Topological Sort (DFS from node 0)
DFS visits: 0 → 1 → 2 → 3 → 4 → 5
Post-order stack: [5, 4, 3, 2, 1, 0]
Reversed (topo order): [0, 1, 2, 3, 4, 5]

STEP 2: Initialize Distances
distance = [0, inf, inf, inf, inf, inf]
           Node: 0   1    2    3    4    5

STEP 3: Process in Topological Order

Process node 0 (distance[0] = 0):
  - Relax edge 0→1 (weight 1): distance[1] = min(inf, 0+1) = 1
  distance = [0, 1, inf, inf, inf, inf]

Process node 1 (distance[1] = 1):
  - Relax edge 1→2 (weight 1): distance[2] = min(inf, 1+1) = 2
  distance = [0, 1, 2, inf, inf, inf]

Process node 2 (distance[2] = 2):
  - Relax edge 2→3 (weight 5): distance[3] = min(inf, 2+5) = 7
  - Relax edge 2→4 (weight 8): distance[4] = min(inf, 2+8) = 10
  distance = [0, 1, 2, 7, 10, inf]

Process node 3 (distance[3] = 7):
  - Relax edge 3→4 (weight 2): distance[4] = min(10, 7+2) = 9 ✓ Updated!
  distance = [0, 1, 2, 7, 9, inf]

Process node 4 (distance[4] = 9):
  - Relax edge 4→5 (weight 1): distance[5] = min(inf, 9+1) = 10
  distance = [0, 1, 2, 7, 9, 10]

Process node 5 (distance[5] = 10):
  - No outgoing edges
  distance = [0, 1, 2, 7, 9, 10]

FINAL RESULT: [0, 1, 2, 7, 9, 10]

Shortest Paths from node 0:
- 0→0: 0
- 0→1: 1 (path: 0→1)
- 0→2: 2 (path: 0→1→2)
- 0→3: 7 (path: 0→1→2→3)
- 0→4: 9 (path: 0→1→2→3→4, NOT 0→1→2→4 which is 10)
- 0→5: 10 (path: 0→1→2→3→4→5)

KEY OBSERVATION:
Node 4 was updated TWICE:
1. First from node 2: distance = 10 (path 0→1→2→4)
2. Then from node 3: distance = 9 (path 0→1→2→3→4)

This works because we process nodes in topological order!
When we process node 3, we already have the optimal distance to node 3,
so we can correctly update node 4.

================================================================================
FANG INTERVIEW TALKING POINTS
================================================================================

1. "I recognize this is a DAG, so I can use topological sort for O(V+E) shortest path"

2. "The key insight is processing nodes in dependency order - when we process a node,
   we've already found its shortest path, so we can safely relax all its edges"

3. "This is better than Dijkstra O((V+E)logV) for DAGs, and unlike Dijkstra,
   it handles negative weights correctly"

4. "Time complexity: O(V+E) for topo sort + O(V+E) for relaxation = O(V+E) total"

5. "Space complexity: O(V) for distance array, visited set, and recursion stack"

6. Edge case handling:
   - Disconnected nodes stay at infinity (unreachable)
   - Negative weights work (unlike Dijkstra)
   - Single node graph works (returns [0])

7. "Real-world applications: project scheduling, build systems, course prerequisites"

COMMON MISTAKES TO AVOID:
- Forgetting to check if distance[node] != inf before relaxing edges
- Not reversing the stack after DFS (wrong topological order)
- Using this on graphs with cycles (will not work - need Dijkstra/Bellman-Ford)
- Confusing with BFS (BFS only works for unweighted graphs)

VARIATIONS TO DISCUSS:
- Longest path in DAG: Same algorithm, just negate weights or use max instead of min
- Critical path method (CPM): Find longest path (project duration)
- Can extend to count number of shortest paths
"""