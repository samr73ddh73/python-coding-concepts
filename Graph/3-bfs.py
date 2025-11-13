from typing import List, Dict, Set, Deque
from collections import deque, defaultdict

"""
BFS (BREADTH-FIRST SEARCH) - FANG INTERVIEW GUIDE

CORE CONCEPT:
- Explores graph level by level (nearest neighbors first)
- Uses QUEUE (FIFO) data structure
- Guarantees shortest path in unweighted graphs

TIME COMPLEXITY: O(V + E)
- Visit each vertex once: O(V)
- Process each edge once: O(E)

SPACE COMPLEXITY: O(V)
- Queue: O(V) in worst case (all vertices in queue)
- Visited set: O(V)
- Total: O(V)

WHEN TO USE BFS vs DFS:
 BFS for:
- Shortest path in unweighted graphs
- Level-order traversal
- Finding connected components
- Minimum steps problems

L Use DFS instead for:
- Topological sort
- Cycle detection
- Path finding (when any path works)
- Backtracking problems
"""

def bfs_basic(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    Basic BFS traversal returning nodes in visit order.

    Time: O(V + E) - visit each vertex once, process each edge once
    Space: O(V) - queue + visited set

    Args:
        graph: Adjacency list as dict
        start: Starting vertex

    Returns:
        List of vertices in BFS order

    Example:
        graph = {0: [1, 2], 1: [3], 2: [3], 3: []}
        bfs_basic(graph, 0) � [0, 1, 2, 3]
    """
    # Edge case: empty graph or invalid start
    if not graph or start not in graph:
        return []

    visited = set()  # O(1) lookup, O(V) space
    queue = deque([start])  # collections.deque is O(1) for append/popleft
    visited.add(start)
    result = []

    while queue:  # O(V) iterations total
        node = queue.popleft()  # O(1) - deque is doubly-linked list
        result.append(node)

        # Process all neighbors
        for neighbor in graph[node]:  # O(degree) per node, O(E) total
            if neighbor not in visited:  # O(1) set lookup
                visited.add(neighbor)  # Mark as visited BEFORE adding to queue!
                queue.append(neighbor)  # O(1)

    return result


def bfs_with_levels(graph: Dict[int, List[int]], start: int) -> Dict[int, int]:
    """
    BFS that tracks distance/level of each vertex from start.

    Time: O(V + E)
    Space: O(V)

    Common in: shortest path, minimum steps problems

    Returns:
        Dict mapping vertex � distance from start

    Example:
        graph = {0: [1, 2], 1: [3], 2: [3], 3: []}
        bfs_with_levels(graph, 0) � {0: 0, 1: 1, 2: 1, 3: 2}
    """
    if not graph or start not in graph:
        return {}

    visited = {start: 0}  # vertex � distance
    queue = deque([start])

    while queue:
        node = queue.popleft()
        current_level = visited[node]

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited[neighbor] = current_level + 1  # Track level
                queue.append(neighbor)

    return visited


def bfs_shortest_path(graph: Dict[int, List[int]], start: int, target: int) -> List[int]:
    """
    Find shortest path from start to target using BFS.

    Time: O(V + E) - worst case explores entire graph
    Space: O(V) - queue + parent tracking

    Returns:
        Shortest path as list of vertices, or [] if no path exists

    Example:
        graph = {0: [1, 2], 1: [3], 2: [3], 3: [4], 4: []}
        bfs_shortest_path(graph, 0, 4) � [0, 1, 3, 4]
    """
    if not graph or start not in graph or target not in graph:
        return []

    if start == target:
        return [start]

    visited = {start}
    queue = deque([start])
    parent = {start: None}  # Track path: child � parent

    while queue:
        node = queue.popleft()

        # Early termination when target found
        if node == target:
            # Reconstruct path from target to start
            path = []
            current = target
            while current is not None:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Reverse to get start � target

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node  # Track parent
                queue.append(neighbor)

    return []  # No path found


def bfs_all_components(graph: Dict[int, List[int]]) -> List[List[int]]:
    """
    Find all connected components using BFS.

    Time: O(V + E) - visits each vertex and edge once
    Space: O(V)

    Returns:
        List of components, where each component is a list of vertices

    Example:
        graph = {0: [1], 1: [0], 2: [3], 3: [2], 4: []}
        bfs_all_components(graph) � [[0, 1], [2, 3], [4]]
    """
    if not graph:
        return []

    visited = set()
    components = []

    for vertex in graph:  # O(V) iterations
        if vertex not in visited:
            # BFS from this vertex
            component = []
            queue = deque([vertex])
            visited.add(vertex)

            while queue:  # O(E) total across all components
                node = queue.popleft()
                component.append(node)

                for neighbor in graph[node]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

            components.append(component)

    return components


def bfs_matrix(matrix: List[List[int]], start_row: int, start_col: int) -> List[tuple]:
    """
    BFS on 2D grid/matrix (common in FANG interviews!).

    Time: O(rows � cols) - visit each cell once
    Space: O(rows � cols) - visited set + queue

    Use cases: Island problems, shortest path in grid, flood fill

    Args:
        matrix: 2D grid
        start_row, start_col: Starting position

    Returns:
        List of (row, col) tuples in BFS order

    Example:
        matrix = [[1,1,0], [1,0,0], [0,0,1]]
        bfs_matrix(matrix, 0, 0) � [(0,0), (0,1), (1,0)]
    """
    if not matrix or not matrix[0]:
        return []

    rows, cols = len(matrix), len(matrix[0])

    # Validate start position
    if not (0 <= start_row < rows and 0 <= start_col < cols):
        return []

    visited = set()
    queue = deque([(start_row, start_col)])
    visited.add((start_row, start_col))
    result = []

    # 4-directional movement: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    # For 8-directional: add diagonals [(-1,-1), (-1,1), (1,-1), (1,1)]

    while queue:
        row, col = queue.popleft()
        result.append((row, col))

        # Explore all 4 neighbors
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            # Check boundaries and visited status
            if (0 <= new_row < rows and
                0 <= new_col < cols and
                (new_row, new_col) not in visited and
                matrix[new_row][new_col] == 1):  # Adjust condition as needed

                visited.add((new_row, new_col))
                queue.append((new_row, new_col))

    return result


def bfs_multi_source(graph: Dict[int, List[int]], sources: List[int]) -> Dict[int, int]:
    """
    Multi-source BFS (start from multiple vertices simultaneously).

    Time: O(V + E)
    Space: O(V)

    Use cases: Rotting oranges, walls and gates, nearest exit

    Returns:
        Dict mapping vertex � minimum distance from ANY source

    Example:
        graph = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
        bfs_multi_source(graph, [0, 3]) � {0: 0, 1: 1, 2: 1, 3: 0}
    """
    if not graph or not sources:
        return {}

    distances = {}
    queue = deque()

    # Initialize: add all sources to queue with distance 0
    for source in sources:
        if source in graph:
            distances[source] = 0
            queue.append(source)

    while queue:
        node = queue.popleft()
        current_dist = distances[node]

        for neighbor in graph[node]:
            if neighbor not in distances:  # Not visited yet
                distances[neighbor] = current_dist + 1
                queue.append(neighbor)

    return distances


"""
PYTHON INTERNALS & OPTIMIZATION TIPS:

1. DEQUE vs LIST for Queue:
    deque: O(1) popleft()
   L list:  O(n) pop(0) - shifts all elements!

   Always use collections.deque for BFS!

2. SET vs LIST for Visited:
    set: O(1) lookup
   L list: O(n) lookup with 'in' operator

   Always use set() for visited tracking!

3. When to Mark as Visited:
   CRITICAL: Mark visited WHEN ADDING TO QUEUE, not when popping!
   L Wrong: Pop node, then mark visited � duplicates in queue
    Right: Mark visited before adding to queue

4. Graph Representation:
   - defaultdict(list) is cleanest (no KeyError)
   - Regular dict works if all vertices have entries
   - For matrix: use index-based access

5. Early Termination:
   - For shortest path: return immediately when target found
   - For existence: return True as soon as condition met
   - Don't traverse entire graph unnecessarily!
"""

# ==================== COMMON BFS PATTERNS ====================

def pattern_level_order_traversal(graph: Dict[int, List[int]], start: int) -> List[List[int]]:
    """
    Pattern: Return nodes grouped by level.
    Used in: Tree level order, word ladder, minimum genetic mutation
    """
    if not graph or start not in graph:
        return []

    levels = []
    queue = deque([start])
    visited = {start}

    while queue:
        level_size = len(queue)  # Process current level
        current_level = []

        for _ in range(level_size):  # Process exactly level_size nodes
            node = queue.popleft()
            current_level.append(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        levels.append(current_level)

    return levels


def pattern_bidirectional_bfs(graph: Dict[int, List[int]], start: int, target: int) -> int:
    """
    Pattern: Bidirectional BFS (search from both ends).
    Time: O(V + E) but typically faster than regular BFS
    Used in: Word ladder, shortest path optimization
    """
    if start == target:
        return 0

    if start not in graph or target not in graph:
        return -1

    # Two frontiers
    front_visited = {start: 0}
    back_visited = {target: 0}
    front_queue = deque([start])
    back_queue = deque([target])

    while front_queue and back_queue:
        # Always expand smaller frontier (optimization)
        if len(front_queue) <= len(back_queue):
            if expand_frontier(graph, front_queue, front_visited, back_visited):
                return True
        else:
            if expand_frontier(graph, back_queue, back_visited, front_visited):
                return True

    return -1  # No path found

def expand_frontier(graph, queue, visited, other_visited):
    """Helper for bidirectional BFS."""
    node = queue.popleft()
    current_dist = visited[node]

    for neighbor in graph[node]:
        if neighbor in other_visited:
            # Frontiers met!
            return True
        if neighbor not in visited:
            visited[neighbor] = current_dist + 1
            queue.append(neighbor)

    return False


# ==================== EDGE CASES TO ALWAYS CONSIDER ====================

"""
FANG INTERVIEW CHECKLIST:

1. Empty/Invalid Input:
   - Empty graph: graph = {}
   - None/null inputs
   - Start vertex not in graph
   - Target vertex not in graph

2. Single Node:
   - graph = {0: []}
   - start == target

3. Disconnected Graph:
   - Unreachable vertices
   - Multiple components

4. Self-Loops:
   - graph = {0: [0, 1], 1: []}
   - Handled by visited set

5. Cycles:
   - graph = {0: [1], 1: [2], 2: [0]}
   - Handled by visited set

6. Complete Graph:
   - Every vertex connects to every other
   - Large queue size

7. For Grid/Matrix:
   - Out of bounds
   - Empty matrix
   - 1x1 matrix
   - Obstacles/blocked cells
"""

# ==================== TEST CASES ====================

def run_tests():
    """Test all BFS implementations."""

    # Test graph
    graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1],
        5: [2]
    }

    print("=== Basic BFS ===")
    print(f"BFS from 0: {bfs_basic(graph, 0)}")
    # Expected: [0, 1, 2, 3, 4, 5]

    print("\n=== BFS with Levels ===")
    levels = bfs_with_levels(graph, 0)
    print(f"Distances from 0: {levels}")
    # Expected: {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2}

    print("\n=== Shortest Path ===")
    path = bfs_shortest_path(graph, 0, 5)
    print(f"Shortest path 0�5: {path}")
    # Expected: [0, 2, 5]

    print("\n=== Connected Components ===")
    disconnected = {
        0: [1], 1: [0],
        2: [3], 3: [2],
        4: []
    }
    components = bfs_all_components(disconnected)
    print(f"Components: {components}")
    # Expected: [[0, 1], [2, 3], [4]]

    print("\n=== Matrix BFS ===")
    matrix = [
        [1, 1, 0],
        [1, 0, 0],
        [0, 0, 1]
    ]
    grid_result = bfs_matrix(matrix, 0, 0)
    print(f"Grid BFS from (0,0): {grid_result}")
    # Expected: [(0, 0), (0, 1), (1, 0)]

    print("\n=== Multi-Source BFS ===")
    multi_dist = bfs_multi_source(graph, [0, 5])
    print(f"Min distances from {0, 5}: {multi_dist}")
    # Expected: {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 0}

    print("\n=== Level Order Traversal ===")
    levels_grouped = pattern_level_order_traversal(graph, 0)
    print(f"Nodes by level: {levels_grouped}")
    # Expected: [[0], [1, 2], [3, 4, 5]]


if __name__ == "__main__":
    run_tests()


"""
COMPLEXITY ANALYSIS SUMMARY:

Algorithm               | Time      | Space     | Use Case
------------------------|-----------|-----------|---------------------------
Basic BFS               | O(V + E)  | O(V)      | Traversal, reachability
BFS with Levels         | O(V + E)  | O(V)      | Shortest path, min steps
Shortest Path           | O(V + E)  | O(V)      | Find actual path
All Components          | O(V + E)  | O(V)      | Connectivity
Matrix BFS              | O(R � C)  | O(R � C)  | Grid problems
Multi-Source BFS        | O(V + E)  | O(V)      | Multiple starting points
Bidirectional BFS       | O(V + E)* | O(V)      | Faster shortest path

*Bidirectional BFS has same worst case but typically 2x faster in practice

SPACE BREAKDOWN:
- Queue: O(V) worst case (all vertices at one level)
- Visited: O(V) always
- Parent/Distance tracking: O(V)
- Total: O(V) for adjacency list representation
"""
