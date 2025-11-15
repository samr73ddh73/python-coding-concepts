"""
================================================================================
PATTERN: Bipartite Graph Detection using BFS/DFS + Graph Coloring
================================================================================

PROBLEM:
Determine if a graph is bipartite. A graph is bipartite if we can color all nodes
with exactly 2 colors such that no two adjacent nodes have the same color.

DEFINITION - What is a Bipartite Graph?
A graph is bipartite if we can divide its vertices into TWO independent sets such that:
1. Every edge connects a vertex from one set to a vertex in the other set
2. No edge exists within the same set
3. Equivalently: Can color graph with 2 colors where no adjacent nodes share color

================================================================================
KEY PROPERTIES OF BIPARTITE GRAPHS:
================================================================================

1. LINEAR GRAPHS (No Cycles):
   - ALL acyclic graphs are bipartite
   - Trees are always bipartite
   Example: 0—1—2—3  (can alternate colors)

2. EVEN-LENGTH CYCLES:
   - Graphs with cycles of EVEN length are bipartite
   - Example: 0—1—2—3—0 (cycle length 4, can alternate colors: 0,1,0,1)

3. ODD-LENGTH CYCLES:
   - Graphs with ANY odd-length cycle are NOT bipartite
   - Example: 0—1—2—0 (cycle length 3, impossible to color with 2 colors)
   - This is the ONLY case where graph is not bipartite

THEOREM: A graph is bipartite ⟺ it contains NO odd-length cycles

================================================================================
ALGORITHM: Graph Coloring via BFS
================================================================================

APPROACH:
1. Use BFS to traverse the graph
2. Color each node with alternating colors (0 and 1)
3. When visiting a neighbor:
   - If unvisited → color it with opposite color of current node
   - If visited → check if it has the correct opposite color
   - If visited neighbor has SAME color → NOT bipartite (odd cycle detected!)
4. Handle disconnected components (graph may not be fully connected)

WHY BFS/DFS WORKS:
- BFS explores level by level, naturally alternating colors
- If we encounter a node already colored with the SAME color as current,
  it means we found an odd-length cycle
- DFS works similarly but explores depth-first

TIME COMPLEXITY: O(V + E)
- V = number of vertices (nodes)
- E = number of edges
- Visit each node once: O(V)
- Check each edge once: O(E)
- Total: O(V + E)

SPACE COMPLEXITY: O(V)
- Color/visited dict: O(V) to store color for each node
- Queue for BFS: O(V) in worst case
- Recursion stack for DFS: O(V) in worst case

================================================================================
REAL-WORLD APPLICATIONS:
================================================================================

1. JOB SCHEDULING / TASK ASSIGNMENT:
   - Assign tasks to two processors/workers
   - Conflicting tasks (edges) must be on different processors
   - If not bipartite → need more than 2 processors

2. MATCHING PROBLEMS:
   - Dating apps: Match two groups (e.g., men and women)
   - Job matching: Candidates ↔ Job positions
   - Maximum bipartite matching algorithms

3. CONFLICT RESOLUTION:
   - Two opposing teams/groups
   - People who conflict (edge) must be in different groups
   - Example: Seating arrangements, team divisions

4. NETWORK DESIGN:
   - Two-layer network topology
   - Switches connecting to servers (no switch-to-switch or server-to-server)
   - Common in data center architectures

5. SOCIAL NETWORKS:
   - Detect if network can be split into two non-interacting groups
   - Friend recommendation systems
   - Community detection

6. STABLE MARRIAGE PROBLEM:
   - Classic bipartite matching problem
   - Used in hospital-resident matching, school admissions

7. IMAGE SEGMENTATION:
   - Divide pixels into foreground/background
   - Graph cut algorithms for image processing

8. COURSE SCHEDULING:
   - Schedule courses into two time slots
   - Courses with common students (edge) → different slots

================================================================================
EDGE CASES:
================================================================================
1. Empty graph → bipartite (vacuously true)
2. Single node → bipartite
3. Disconnected graph → check each component separately
4. Complete graph K_n:
   - K_2 (two nodes, one edge) → bipartite
   - K_3+ (three or more fully connected) → NOT bipartite (contains triangles)
5. Self-loop → NOT bipartite (odd cycle of length 1)
6. Graph with no edges → bipartite (all nodes can be same color, but technically valid)

PYTHON INTERNALS:
- dict for color storage: O(1) lookup/insert
- deque for BFS: O(1) append/popleft
- Could use list of size n, but dict handles sparse graphs better
"""

from collections import deque
from typing import List

class Solution:
    """
    BFS Approach - Graph Coloring
    TIME: O(V + E) | SPACE: O(V)
    """
    def isBipartite(self, graph: List[List[int]]) -> bool:
        visited = {}  # Store color for each node (0 or 1)
        queue = deque()

        # Check each component (graph might be disconnected)
        for i in range(len(graph)):
            if i in visited:
                continue  # Already processed this component

            # Start BFS from this node with color 1
            queue.append(i)
            visited[i] = 1

            while queue:
                node = queue.popleft()

                # Try to color all neighbors with opposite color
                for neighbor in graph[node]:
                    color = 1 if visited[node] == 0 else 0  # Opposite color

                    if neighbor not in visited:
                        # First time visiting, assign opposite color
                        queue.append(neighbor)
                        visited[neighbor] = color
                    elif visited[neighbor] != color:
                        # Already visited with SAME color → odd cycle found!
                        return False

        return True  # All components are bipartite


# ============================================================================
# ALTERNATIVE: DFS Approach
# ============================================================================
class SolutionDFS:
    """
    DFS Approach - Graph Coloring (Recursive)
    TIME: O(V + E) | SPACE: O(V)
    """
    def isBipartite(self, graph: List[List[int]]) -> bool:
        color = {}  # -1: not colored, 0: color 0, 1: color 1

        def dfs(node: int, c: int) -> bool:
            """
            Try to color node with color c
            Returns False if conflict found (not bipartite)
            """
            if node in color:
                return color[node] == c  # Check if consistent

            color[node] = c  # Color this node

            # Try to color all neighbors with opposite color
            for neighbor in graph[node]:
                if not dfs(neighbor, 1 - c):  # 1-c flips between 0 and 1
                    return False

            return True

        # Check all components
        for i in range(len(graph)):
            if i not in color:
                if not dfs(i, 0):  # Start with color 0
                    return False

        return True


"""
================================================================================
VISUAL EXAMPLES:
================================================================================

Example 1: BIPARTITE (Even cycle)
Graph: 0—1—3—2—0 (cycle of length 4)

  0(Red)  ←→  1(Blue)
    ↕           ↕
  2(Red)  ←→  3(Blue)

Coloring: {0:Red, 1:Blue, 2:Red, 3:Blue}
Result: BIPARTITE ✓

---

Example 2: NOT BIPARTITE (Odd cycle - Triangle)
Graph: 0—1—2—0 (cycle of length 3)

    0(Red)
   ↗  ↖
  1    2
   ↘  ↙

Try coloring:
- Color 0: Red
- Color 1: Blue (neighbor of 0)
- Color 2: Blue (neighbor of 0)
- But 1 and 2 are neighbors! Both Blue → CONFLICT!

Result: NOT BIPARTITE ✗

---

Example 3: BIPARTITE (Tree/Linear)
Graph: 0—1—2—3—4

0(Red)—1(Blue)—2(Red)—3(Blue)—4(Red)

All acyclic graphs are bipartite ✓

---

Example 4: NOT BIPARTITE (Pentagon - Odd cycle of 5)
Graph: 0—1—2—3—4—0 (cycle of length 5)

         0
       ↗   ↖
      4     1
      ↓     ↓
      3  ←  2

Try coloring (0:Red, 1:Blue, 2:Red, 3:Blue, 4:Red)
But 4 and 0 are neighbors, both Red → CONFLICT!

Result: NOT BIPARTITE ✗

================================================================================
INTERVIEW TALKING POINTS:
================================================================================

1. "I recognize this as a bipartite detection problem using graph coloring"
2. "The key insight: bipartite ⟺ no odd-length cycles"
3. "I'll use BFS to color nodes with alternating colors (0 and 1)"
4. "If I encounter a neighbor with the same color, there's an odd cycle"
5. "Need to check all components since graph might be disconnected"
6. "Time: O(V+E), Space: O(V) for color tracking"

COMMON MISTAKES TO AVOID:
- Forgetting to handle disconnected components
- Not using opposite color for neighbors
- Using visited set instead of color map (need to track which color!)
"""