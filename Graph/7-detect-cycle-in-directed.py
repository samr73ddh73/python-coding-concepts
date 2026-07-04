"""
CYCLE DETECTION: DIRECTED vs UNDIRECTED — Why Different Approaches?

🔴 UNDIRECTED: Parent Check is ENOUGH
🔵 DIRECTED: Need pathVisited (parent check FAILS!)

═══════════════════════════════════════════════════════════════════

UNDIRECTED GRAPH — Why Parent Check Works
═══════════════════════════════════════════

In UNDIRECTED graphs: Every edge is BIDIRECTIONAL (A-B means both A→B AND B→A)

Example: 0 — 1 — 2
         |_______|

DFS from 0, parent=-1:
  Visit 0 (parent=-1), neighbors=[1, 2]
    → Add 1 to queue (parent=0)
  Visit 1 (parent=0), neighbors=[0, 2]
    → See 0: visited ✓, but is parent=0 ✓ → SKIP (it's the edge we came from)
    → See 2: not visited → explore
  Visit 2 (parent=1), neighbors=[0, 1]
    → See 0: visited ✓, but is parent=1? NO → CYCLE! ✅
    → See 1: visited ✓, but is parent=1 ✓ → SKIP

✅ Why parent check works:
   - Only ONE path to each node (parent)
   - If we see visited node that's NOT parent → different path → CYCLE
   - Parent check prevents counting the edge we came from

═══════════════════════════════════════════════════════════════════

DIRECTED GRAPH — Why Parent Check FAILS
═════════════════════════════════════════

In DIRECTED graphs: Edges are ONE-DIRECTIONAL (A→B is DIFFERENT from B→A)

Example 1: No Cycle (Cross Edge)
    0 → 1
    ↓   ↓
    2 → 3

DFS from 0:
  Visit 0 (parent=-1), neighbors=[1, 2]
    → Explore 1 first
  Visit 1 (parent=0), neighbors=[3]
    → Explore 3
  Visit 3 (parent=1), neighbors=[]
    → Backtrack to 1, backtrack to 0
  Visit 2 (parent=0), neighbors=[3]
    → See 3: already visited, is parent=0? NO!

❌ WRONG conclusion with parent check: "3 is visited and not parent → CYCLE!"
✅ CORRECT: No cycle! (0→1→3) and (0→2→3) just meet at 3 (cross edge, NOT cycle)

Example 2: With Cycle
    0 → 1 → 2
        ↑   |
        └───┘

DFS from 0:
  Visit 0, neighbors=[1]
    → Explore 1
  Visit 1, neighbors=[2]
    → Explore 2
  Visit 2, neighbors=[1]
    → See 1: visited, parent=1? NO!

❌ WRONG with parent check: "1 is visited and not parent → CYCLE!"
    This LOOKS like the above example, but it actually IS a cycle!

😱 PARENT CHECK CAN'T DISTINGUISH:
   - Cross edges (different branches meeting) → NOT a cycle
   - Back edges (loop in current path) → IS a cycle

═══════════════════════════════════════════════════════════════════

✅ SOLUTION: Use pathVisited (Current DFS Path)

Example with pathVisited:

No Cycle Case:
    0 → 1
    ↓   ↓
    2 → 3

DFS(0): pathVisited={0}
  Visit 1: pathVisited={0,1}
    Visit 3: pathVisited={0,1,3}
    Backtrack: pathVisited={0,1}, REMOVE 3 from pathVisited! ⭐

  Visit 2: pathVisited={0,2}
    Visit 3: pathVisited={0,2,3}
    See 3 is in visited ✓
    Is 3 in pathVisited={0,2,3}? YES!

Wait... that's wrong. Let me retrace:

DFS(0): pathVisited={0}
  Visit 1: pathVisited={0,1}
    Visit 3: pathVisited={0,1,3}
    Backtrack: pathVisited={0,1}, REMOVE 3! pathVisited={0,1}
  Backtrack from 1: pathVisited={0}, REMOVE 1! pathVisited={0}

  Visit 2: pathVisited={0,2}
    Visit 3: pathVisited={0,2,3}
    Is 3 already visited? YES
    But is 3 in pathVisited={0,2,3}? YES...

Hmm, let me think about this differently.

Actually the key is:
- When we finish exploring 1 completely, we remove 1 from pathVisited
- When we finish exploring 3 from path 0→1→3, we remove 3 from pathVisited
- ONLY when we encounter a node that's CURRENTLY in our path (in pathVisited)
  do we have a cycle

No Cycle Example (corrected):
    0 → 1 → 3
    └→ 2 → 3

DFS(0, pathVisited={0}):
  Neighbor 1: DFS(1, pathVisited={0,1}):
    Neighbor 3: DFS(3, pathVisited={0,1,3}):
      No neighbors
      Return, remove 3: pathVisited={0,1}
    Return, remove 1: pathVisited={0}

  Neighbor 2: DFS(2, pathVisited={0,2}):
    Neighbor 3: seen in visited ✓
    Is 3 in pathVisited={0,2}? NO! → Not in current path → Safe (cross edge)
    Return, remove 2: pathVisited={0}

✅ Correctly identifies: NO CYCLE

Cycle Example:
    0 → 1 → 2
        ↑   |
        └───┘

DFS(0, pathVisited={0}):
  Neighbor 1: DFS(1, pathVisited={0,1}):
    Neighbor 2: DFS(2, pathVisited={0,1,2}):
      Neighbor 1: 1 is in visited ✓
      Is 1 in pathVisited={0,1,2}? YES! → CYCLE! ✅
      Return True (cycle found)

✅ Correctly identifies: CYCLE EXISTS

═══════════════════════════════════════════════════════════════════

KEY DIFFERENCES:
════════════════

UNDIRECTED:
  - Every edge bidirectional → Only parent check needed
  - Parent = the edge we came from
  - Any visited non-parent = different path = cycle

DIRECTED:
  - Edges one-directional → Parent check NOT enough
  - Need to know: "Is this node in the CURRENT DFS path?"
  - pathVisited = nodes in current recursion stack = current DFS path
  - If neighbor in pathVisited → back edge in current path → CYCLE
  - If neighbor in visited but NOT in pathVisited → cross/forward edge → SAFE

═══════════════════════════════════════════════════════════════════

Time/Space Complexity:
  TIME: O(V + E) - visit each vertex once, each edge once
  SPACE: O(V) - visited + pathVisited + recursion stack

Backtracking (line 102):
  pathVisited.remove(start)
  Remove node AFTER exploring ALL neighbors
  This way, other branches can visit this node without false positives
"""

from typing import List
from collections import defaultdict


class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Course Schedule = Cycle Detection in Directed Graph

        If there's a cycle → impossible to finish all courses
        No cycle → topological order exists → can finish

        Time: O(V + E) where V = numCourses, E = len(prerequisites)
        Space: O(V)
        """
        if len(prerequisites) == 0 or numCourses == 0:
            return True
        graph = self.createGraph(numCourses, prerequisites)
        visited = set()
        pathVisited = set()

        # Check each component (graph might be disconnected)
        for i in range(numCourses):
            if i not in visited:
                if self.dfsHasCycle(graph, i, visited, pathVisited) == True:
                    return False  # Found cycle → can't finish
        return True  # No cycle → can finish

    def dfsHasCycle(self, graph, start, visited, pathVisited):
        """
        DFS with backtracking to detect cycle.

        Returns True if cycle found, False otherwise.
        """
        visited.add(start)
        pathVisited.add(start)  # Add to current path

        for neighbor in graph[start]:
            # Case 1: Back edge found (neighbor in current path)
            if neighbor in visited and neighbor in pathVisited:
                return True  # CYCLE DETECTED!

            # Case 2: Unvisited neighbor - explore it
            if neighbor not in visited:
                if self.dfsHasCycle(graph, neighbor, visited, pathVisited) == True:
                    return True  # Cycle found in deeper recursion

            # Case 3: neighbor in visited but NOT in pathVisited
            # This is a cross edge or forward edge - SAFE (no cycle)

        pathVisited.remove(start)  # Backtrack - remove from current path
        return False  # No cycle found from this node

    def createGraph(self, numCourses, prereq):
        """Build adjacency list from edge list."""
        graph = defaultdict(list)
        for x, y in prereq:
            graph[y].append(x)  # y → x (y is prerequisite for x)
        return graph


# """
# QUICK REVISION CHECKLIST:
# ========================
# ✅ Time: O(V + E) - each vertex visited once, each edge checked once
# ✅ Space: O(V) - two sets + recursion stack
# ✅ Two sets needed: visited (global) + pathVisited (current DFS path)
# ✅ Cycle = node found in pathVisited (back edge in current path)
# ✅ Backtrack: Remove from pathVisited after exploring
# ✅ Handle disconnected components: Loop through all unvisited nodes

# COMMON MISTAKES:
# ================
# ❌ Only using visited set → Can't distinguish cross edges from back edges
# ❌ Forgetting pathVisited.remove(start) → False positives
# ❌ Not checking disconnected components → Missing cycles
# ❌ Using BFS → Can't detect cycles in directed graphs reliably
