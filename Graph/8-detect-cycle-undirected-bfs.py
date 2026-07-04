# UNDIRECTED GRAPH CYCLE DETECTION - BFS
#
# KEY CONCEPT: Parent Check
# In undirected graphs, every edge goes BOTH ways: A-B means A→B AND B→A
# When we visit B from A, A becomes the parent of B.
# When we check B's neighbors, we'll see A is already visited.
# BUT THIS IS NOT A CYCLE - it's just the edge we came from!
#
# We need to check if the visited neighbor is the PARENT:
# - If neighbor is visited AND is parent → skip (it's the edge we came from)
# - If neighbor is visited AND is NOT parent → CYCLE FOUND! (different path to same node)
#
# EXAMPLE:
# Graph:  0 — 1 — 2
#         |_______|
#
# BFS from 0:
#   Visit 0 (parent=-1), add 1,2 to queue
#   Visit 1 (parent=0), neighbors=[0,2]
#     - 0 is visited BUT is parent → SKIP (not a cycle)
#     - 2 not visited → add to queue
#   Visit 2 (parent=0), neighbors=[0,1]
#     - 0 is visited AND is parent → SKIP
#     - 1 is visited AND NOT parent → CYCLE DETECTED! ✓
#        (because we reached 2 from 0 directly AND from 1)
#
# WITHOUT parent check: Would return True at first visited node (WRONG!)
# WITH parent check: Correctly identifies actual cycles (CORRECT!)

from collections import deque

def detectCycleBfs(graph, n):
    queue = deque()
    visited = set()

    for i in range(n):
        if i not in visited:
            queue.append((i, -1))  # (node, parent) - parent=-1 for start
            visited.add(i)
            while queue:
                node, parent = queue.popleft()
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        queue.append((neighbor, node))  # Store parent for cycle check
                        visited.add(neighbor)
                    # CRITICAL: Check if neighbor is NOT parent before declaring cycle
                    elif neighbor in visited and neighbor != parent:
                        return True  # Different path to visited node = CYCLE
    return False        

