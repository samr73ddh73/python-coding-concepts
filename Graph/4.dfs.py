from typing import List, Dict, Set
from collections import defaultdict

"""
DFS (DEPTH-FIRST SEARCH) - FANG INTERVIEW GUIDE

CORE CONCEPT:
- Explores graph depth-first (go as deep as possible before backtracking)
- Uses STACK (LIFO) data structure OR recursion (implicit call stack)
- Two implementations: Recursive (cleaner) vs Iterative (explicit stack)

TIME COMPLEXITY: O(V + E)
- Visit each vertex once: O(V)
- Process each edge once: O(E)
- Same as BFS!

SPACE COMPLEXITY:
- Recursive: O(V) for visited set + O(H) for call stack (H = height/depth)
- Iterative: O(V) for visited set + O(V) for explicit stack
- Worst case: O(V) total

WHEN TO USE DFS vs BFS:
✅ DFS for:
- Topological sort
- Cycle detection
- Path existence (any path, not shortest)
- Backtracking problems
- Connected components
- Tree traversals (pre/in/post-order)

✅ BFS for:
- Shortest path in unweighted graphs
- Level-order traversal
- Minimum steps problems

KEY DIFFERENCE: DFS goes DEEP, BFS goes WIDE
"""

# ============================================================
# METHOD 1: Recursive DFS (Most Common in Interviews!)
# ============================================================

def dfs_recursive(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    Standard recursive DFS.

    Time Complexity: O(V + E)
        - Visit each vertex once: O(V)
        - Explore each edge once: O(E)

    Space Complexity: O(V)
        - visited set: O(V)
        - Call stack: O(H) where H is graph height/depth
        - Worst case (linear chain): O(V)
        - Best case (balanced tree): O(log V)

    ✅ CLEANEST and MOST COMMON in interviews!

    Example:
        graph = {0: [1, 2], 1: [3], 2: [4], 3: [], 4: []}
        dfs_recursive(graph, 0) → [0, 1, 3, 2, 4]
    """
    if not graph or start not in graph:
        return []

    visited = set()
    result = []

    def dfs_helper(node: int):
        """Helper function for recursion."""
        visited.add(node)  # Mark as visited
        result.append(node)

        # Explore all neighbors
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs_helper(neighbor)  # Recursive call

    dfs_helper(start)
    return result


def dfs_recursive_with_path(graph: Dict[int, List[int]], start: int, target: int) -> List[int]:
    """
    Recursive DFS that finds a path from start to target.

    Time: O(V + E) - worst case explores entire graph
    Space: O(V) - visited + call stack

    Returns:
        Path from start to target, or [] if no path exists
    """
    if not graph or start not in graph or target not in graph:
        return []

    visited = set()

    def dfs_path_helper(node: int, path: List[int]) -> List[int]:
        """Helper that returns path if target found."""
        if node == target:
            return path + [node]

        visited.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                result = dfs_path_helper(neighbor, path + [node])
                if result:  # Path found!
                    return result

        return []  # No path found from this branch

    return dfs_path_helper(start, [])


# ============================================================
# METHOD 2: Iterative DFS with Explicit Stack (Important!)
# ============================================================

def dfs_iterative(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    Iterative DFS using explicit stack.

    Time Complexity: O(V + E)
        - Same as recursive version
        - Visit each vertex once
        - Process each edge once

    Space Complexity: O(V)
        - visited set: O(V)
        - Explicit stack: O(V) worst case
        - No call stack overhead!

    Advantages over recursive:
        - No risk of stack overflow on deep graphs
        - Better control over traversal order
        - Can be paused/resumed

    ⚠️ IMPORTANT: The order may differ from recursive DFS!
       - Stack processes neighbors in reverse order
       - To match recursive order: reverse neighbor list before adding

    Example:
        graph = {0: [1, 2], 1: [3], 2: [4], 3: [], 4: []}
        dfs_iterative(graph, 0) → [0, 2, 4, 1, 3] (different from recursive!)
    """
    if not graph or start not in graph:
        return []

    visited = set()
    stack = [start]  # Use list as stack
    result = []

    while stack:
        node = stack.pop()  # O(1) - pop from end (LIFO)

        if node in visited:
            continue

        visited.add(node)
        result.append(node)

        # Add neighbors to stack (in reverse order to match recursive DFS)
        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                stack.append(neighbor)  # O(1)

    return result


def dfs_iterative_alternative(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    Alternative iterative DFS - mark visited BEFORE adding to stack.

    This version matches BFS pattern more closely and avoids duplicates in stack.

    Time: O(V + E)
    Space: O(V)
    """
    if not graph or start not in graph:
        return []

    visited = set()
    stack = [start]
    visited.add(start)  # Mark visited immediately
    result = []

    while stack:
        node = stack.pop()  # Pop from end (LIFO)
        result.append(node)

        # Process neighbors
        for neighbor in reversed(graph[node]):
            if neighbor not in visited:
                visited.add(neighbor)  # Mark before adding to stack
                stack.append(neighbor)

    return result


# ============================================================
# METHOD 3: DFS for Specific Use Cases
# ============================================================

def dfs_all_paths(graph: Dict[int, List[int]], start: int, target: int) -> List[List[int]]:
    """
    Find ALL paths from start to target using DFS + backtracking.

    Time: O(V!) in worst case (complete graph)
        - Can visit same node in different paths
        - Exponential in nature

    Space: O(V) for recursion depth

    Common in: Path finding, combination problems
    """
    if not graph or start not in graph or target not in graph:
        return []

    all_paths = []

    def dfs_backtrack(node: int, path: List[int], visited: Set[int]):
        """Backtracking helper."""
        if node == target:
            all_paths.append(path.copy())  # Found a path!
            return

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                path.append(neighbor)

                dfs_backtrack(neighbor, path, visited)

                # BACKTRACK: remove neighbor for next iteration
                path.pop()
                visited.remove(neighbor)

    # Start DFS
    visited = {start}
    dfs_backtrack(start, [start], visited)
    return all_paths


def dfs_cycle_detection_directed(graph: Dict[int, List[int]]) -> bool:
    """
    Detect cycle in DIRECTED graph using DFS.

    Time: O(V + E)
    Space: O(V)

    Key insight: Track nodes in current recursion stack!
        - visited: nodes we've seen
        - rec_stack: nodes in current DFS path

    Cycle exists if we reach a node already in rec_stack.

    Example:
        graph = {0: [1], 1: [2], 2: [0]}  # Has cycle: 0→1→2→0
        Returns: True
    """
    if not graph:
        return False

    visited = set()
    rec_stack = set()  # Nodes in current recursion path

    def has_cycle(node: int) -> bool:
        visited.add(node)
        rec_stack.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                if has_cycle(neighbor):
                    return True
            elif neighbor in rec_stack:  # Back edge found!
                return True

        rec_stack.remove(node)  # Remove from recursion stack
        return False

    # Check each component
    for node in graph:
        if node not in visited:
            if has_cycle(node):
                return True

    return False


def dfs_cycle_detection_undirected(graph: Dict[int, List[int]]) -> bool:
    """
    Detect cycle in UNDIRECTED graph using DFS.

    Time: O(V + E)
    Space: O(V)

    Key difference from directed: track parent to avoid false positives.

    Cycle exists if we reach a visited node that's NOT our parent.

    Example:
        graph = {0: [1, 2], 1: [0, 2], 2: [0, 1]}  # Triangle - has cycle
        Returns: True
    """
    if not graph:
        return False

    visited = set()

    def has_cycle(node: int, parent: int) -> bool:
        visited.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                if has_cycle(neighbor, node):
                    return True
            elif neighbor != parent:  # Visited and not parent = cycle!
                return True

        return False

    # Check each component
    for node in graph:
        if node not in visited:
            if has_cycle(node, -1):
                return True

    return False


def dfs_topological_sort(graph: Dict[int, List[int]], n: int) -> List[int]:
    """
    Topological sort using DFS (for Directed Acyclic Graphs only).

    Time: O(V + E)
    Space: O(V)

    Algorithm:
        1. Perform DFS
        2. Add node to result AFTER visiting all its descendants
        3. Reverse result at the end

    Use cases: Task scheduling, build dependencies, course prerequisites

    Example:
        graph = {0: [1, 2], 1: [3], 2: [3], 3: []}
        Topological order: [0, 2, 1, 3] or [0, 1, 2, 3]
    """
    visited = set()
    stack = []  # Store topological order

    def dfs_topo(node: int):
        visited.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs_topo(neighbor)

        # Add to stack AFTER exploring all descendants
        stack.append(node)

    # Process all nodes
    for node in range(n):
        if node not in visited and node in graph:
            dfs_topo(node)

    return stack[::-1]  # Reverse for topological order


def dfs_connected_components(graph: Dict[int, List[int]]) -> List[List[int]]:
    """
    Find all connected components using DFS.

    Time: O(V + E)
    Space: O(V)

    Works for both directed and undirected graphs.
    """
    if not graph:
        return []

    visited = set()
    components = []

    def dfs_component(node: int, component: List[int]):
        visited.add(node)
        component.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs_component(neighbor, component)

    for node in graph:
        if node not in visited:
            component = []
            dfs_component(node, component)
            components.append(component)

    return components


# ============================================================
# DFS vs BFS COMPARISON
# ============================================================

"""
RECURSIVE DFS vs ITERATIVE DFS vs BFS:

┌──────────────────┬─────────────┬─────────────┬─────────────┐
│ Aspect           │ Recursive   │ Iterative   │ BFS         │
│                  │ DFS         │ DFS         │             │
├──────────────────┼─────────────┼─────────────┼─────────────┤
│ Data Structure   │ Call stack  │ Explicit    │ Queue       │
│                  │ (implicit)  │ stack       │ (deque)     │
├──────────────────┼─────────────┼─────────────┼─────────────┤
│ Time             │ O(V + E)    │ O(V + E)    │ O(V + E)    │
├──────────────────┼─────────────┼─────────────┼─────────────┤
│ Space            │ O(V)        │ O(V)        │ O(V)        │
│                  │ +O(H) stack │ +O(V) stack │ +O(W) queue │
├──────────────────┼─────────────┼─────────────┼─────────────┤
│ Code Simplicity  │ ⭐⭐⭐⭐⭐   │ ⭐⭐⭐      │ ⭐⭐⭐⭐    │
├──────────────────┼─────────────┼─────────────┼─────────────┤
│ Stack Overflow?  │ Yes (deep)  │ No          │ No          │
├──────────────────┼─────────────┼─────────────┼─────────────┤
│ Traversal Order  │ Deep first  │ Deep first* │ Level by    │
│                  │             │             │ level       │
└──────────────────┴─────────────┴─────────────┴─────────────┘

*Iterative DFS order may differ from recursive due to stack processing

H = maximum depth/height of graph
W = maximum width/level of graph

SPACE COMPLEXITY DETAILS:

1. Recursive DFS:
   - Visited set: O(V)
   - Call stack depth: O(H)
   - Worst case (linear chain): H = V → O(V)
   - Best case (balanced tree): H = log V → O(log V)

2. Iterative DFS:
   - Visited set: O(V)
   - Explicit stack: O(V) worst case
   - All nodes could be in stack before any are processed

3. BFS:
   - Visited set: O(V)
   - Queue: O(W) where W is max width
   - Worst case (complete graph): W ≈ V → O(V)
"""

# ============================================================
# PYTHON STACK INTERNALS
# ============================================================

"""
PYTHON LISTS AS STACKS:

Lists are perfect for stacks in Python!

Operations:
    stack.append(x)  → O(1) amortized - add to end
    stack.pop()      → O(1) - remove from end
    stack[-1]        → O(1) - peek at top

Why not use collections.deque for stack?
    - Lists are slightly faster for stack operations
    - deque is optimized for double-ended operations
    - For pure stack usage, list is preferred!

    Benchmark (1M operations):
        list.append() + pop()  → ~0.08s
        deque.append() + pop() → ~0.12s

CALL STACK:

When you use recursive DFS:
    - Python maintains implicit call stack
    - Each function call adds a frame to stack
    - Stack frame contains: local variables, return address, parameters

    def dfs(node):
        visited.add(node)      # Frame 1
        for n in graph[node]:
            dfs(n)             # Frame 2 pushed onto Frame 1
                               # Frame 3 pushed onto Frame 2
                               # ...

    Stack depth limited by sys.getrecursionlimit() (default ~1000-3000)

STACK OVERFLOW:

Python recursive DFS can fail on deep graphs!

    graph = {i: [i+1] for i in range(10000)}  # Linear chain
    dfs_recursive(graph, 0)  # RecursionError!

Solution:
    1. Use iterative DFS (no recursion limit!)
    2. Increase limit: sys.setrecursionlimit(10000)
       ⚠️  Risky - can crash Python interpreter
    3. Restructure algorithm if possible
"""

# ============================================================
# PERFORMANCE COMPARISON
# ============================================================

def compare_dfs_methods():
    """Compare recursive vs iterative DFS performance."""
    import time

    # Build test graph
    graph = defaultdict(list)
    n = 1000

    # Create linear chain: 0→1→2→...→999
    for i in range(n - 1):
        graph[i].append(i + 1)

    print("=== DFS PERFORMANCE COMPARISON (1000 vertices) ===\n")

    # Recursive DFS
    start = time.perf_counter()
    result1 = dfs_recursive(graph, 0)
    time1 = time.perf_counter() - start
    print(f"1. Recursive DFS:       {time1*1000:.3f}ms")

    # Iterative DFS
    start = time.perf_counter()
    result2 = dfs_iterative(graph, 0)
    time2 = time.perf_counter() - start
    print(f"2. Iterative DFS:       {time2*1000:.3f}ms")

    # Alternative iterative
    start = time.perf_counter()
    result3 = dfs_iterative_alternative(graph, 0)
    time3 = time.perf_counter() - start
    print(f"3. Iterative (alt):     {time3*1000:.3f}ms")

    print(f"\nAll methods visited {len(result1)} nodes")
    print(f"Note: Order may differ between methods")


# ============================================================
# TEST CASES
# ============================================================

def run_tests():
    """Test all DFS implementations."""

    # Test graph
    graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1],
        5: [2]
    }

    print("=== Testing DFS Implementations ===\n")

    print("1. Recursive DFS:")
    print(f"   Result: {dfs_recursive(graph, 0)}")

    print("\n2. Iterative DFS:")
    print(f"   Result: {dfs_iterative(graph, 0)}")

    print("\n3. Iterative DFS (alternative):")
    print(f"   Result: {dfs_iterative_alternative(graph, 0)}")

    print("\n4. DFS Path Finding:")
    path = dfs_recursive_with_path(graph, 0, 5)
    print(f"   Path 0→5: {path}")

    print("\n5. All Paths (0→5):")
    all_paths = dfs_all_paths(graph, 0, 5)
    for i, p in enumerate(all_paths, 1):
        print(f"   Path {i}: {p}")

    print("\n6. Cycle Detection (Directed):")
    cycle_graph = {0: [1], 1: [2], 2: [0]}
    has_cycle = dfs_cycle_detection_directed(cycle_graph)
    print(f"   Graph {cycle_graph} has cycle: {has_cycle}")

    print("\n7. Topological Sort:")
    dag = {0: [1, 2], 1: [3], 2: [3], 3: []}
    topo_order = dfs_topological_sort(dag, 4)
    print(f"   Topological order: {topo_order}")

    print("\n8. Connected Components:")
    disconnected = {
        0: [1], 1: [0],
        2: [3], 3: [2],
        4: []
    }
    components = dfs_connected_components(disconnected)
    print(f"   Components: {components}")

    print("\n" + "="*60)
    compare_dfs_methods()


if __name__ == "__main__":
    run_tests()


"""
==================== FANG INTERVIEW SUMMARY ====================

DFS COMPLEXITY CHEAT SHEET:

Algorithm                    | Time      | Space     | Use Case
-----------------------------|-----------|-----------|------------------
Recursive DFS                | O(V + E)  | O(V)      | Most problems
Iterative DFS                | O(V + E)  | O(V)      | Deep graphs
DFS Path Finding             | O(V + E)  | O(V)      | Find a path
DFS All Paths                | O(V!)     | O(V)      | Backtracking
Cycle Detection (Directed)   | O(V + E)  | O(V)      | DAG validation
Cycle Detection (Undirected) | O(V + E)  | O(V)      | Tree validation
Topological Sort             | O(V + E)  | O(V)      | Task ordering
Connected Components         | O(V + E)  | O(V)      | Graph clustering

==================== KEY INSIGHTS ====================

1. RECURSIVE vs ITERATIVE:
   - Recursive: Cleaner code, risk of stack overflow
   - Iterative: Safer for deep graphs, more control
   - Both have same time complexity: O(V + E)

2. CALL STACK vs EXPLICIT STACK:
   - Call stack: Managed by Python, limited depth (~1000-3000)
   - Explicit stack: Managed by you, unlimited (until memory runs out)

3. DFS vs BFS:
   - DFS: Go deep (stack/recursion)
   - BFS: Go wide (queue)
   - Same time complexity, different traversal patterns

4. WHEN TO USE DFS:
   ✅ Topological sort (MUST use DFS)
   ✅ Cycle detection (easier with DFS)
   ✅ Path existence (DFS is simpler)
   ✅ Backtracking problems
   ❌ Shortest path (use BFS)
   ❌ Level-order traversal (use BFS)

==================== COMMON MISTAKES ====================

❌ 1. Forgetting to mark node as visited
       → Infinite recursion/loop

❌ 2. Marking visited after recursive call
       → Duplicate processing

❌ 3. Using recursion on very deep graphs
       → RecursionError

❌ 4. Not handling disconnected components
       → Missing parts of graph

✅ CORRECT PATTERN:

   def dfs(node):
       visited.add(node)  # Mark FIRST
       process(node)
       for neighbor in graph[node]:
           if neighbor not in visited:
               dfs(neighbor)

==================== INTERVIEW TIPS ====================

1. Always ask: "Can I use recursion?"
   - Some interviewers want iterative solution
   - Some graphs too deep for recursion

2. Mention trade-offs:
   - "I'll use recursive DFS for cleaner code, but we could
      use iterative if the graph might be very deep"

3. State complexity explicitly:
   - "This is O(V+E) time because we visit each vertex once
      and explore each edge once"

4. Consider the call stack:
   - "The space complexity includes O(H) for the call stack
      where H is the depth, which is O(V) in worst case"
"""
