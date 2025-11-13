"""
CYCLE DETECTION IN DIRECTED GRAPH - QUICK REVISION

TIME COMPLEXITY: O(V + E)
- Visit each vertex once: O(V)
- Process each edge once: O(E)

SPACE COMPLEXITY: O(V)
- visited set: O(V)
- pathVisited set: O(V)
- Recursion stack: O(V) in worst case (chain graph)

WHY TWO SETS? (visited + pathVisited)
================================

visited:      Tracks ALL nodes explored in ANY DFS path
pathVisited:  Tracks nodes ONLY in CURRENT DFS path (recursion stack)

KEY INSIGHT: Cycle = finding a node that's in the CURRENT path (pathVisited)

VISUAL EXAMPLE:
    0 → 1 → 2
        ↑   |
        3 ← ┘

DFS from 0:
1. Visit 0: visited={0}, pathVisited={0}
2. Visit 1: visited={0,1}, pathVisited={0,1}
3. Visit 2: visited={0,1,2}, pathVisited={0,1,2}
4. Visit 3: visited={0,1,2,3}, pathVisited={0,1,2,3}
5. Try 1 again: 1 ∈ pathVisited → CYCLE FOUND! ✅

After backtrack from 3:
   pathVisited={0,1,2} (removed 3)

WHY NOT JUST visited?
If we only had visited, we'd see: "1 ∈ visited → cycle?"
But NO! We could've visited 1 from a DIFFERENT path (disconnected component).
pathVisited tells us: "1 is in THIS EXACT DFS PATH" → TRUE CYCLE

BACKTRACKING (line 24):
pathVisited.remove(start) — Remove node from current path when done exploring
This allows other branches to visit this node safely.


INTERVIEW TIP:
==============
Mention: "I'm checking pathVisited first because it's more specific -
if a node is in the current path, we found a back edge, which means a cycle."
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


"""
QUICK REVISION CHECKLIST:
========================
✅ Time: O(V + E) - each vertex visited once, each edge checked once
✅ Space: O(V) - two sets + recursion stack
✅ Two sets needed: visited (global) + pathVisited (current DFS path)
✅ Cycle = node found in pathVisited (back edge in current path)
✅ Backtrack: Remove from pathVisited after exploring
✅ Handle disconnected components: Loop through all unvisited nodes

COMMON MISTAKES:
================
❌ Only using visited set → Can't distinguish cross edges from back edges
❌ Forgetting pathVisited.remove(start) → False positives
❌ Not checking disconnected components → Missing cycles
❌ Using BFS → Can't detect cycles in directed graphs reliably
