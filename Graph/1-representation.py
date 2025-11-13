from typing import List

"""
GRAPH REPRESENTATION - TIME & SPACE COMPLEXITY GUIDE

ADJACENCY MATRIX:
- Space: O(V²) - Always uses V×V array regardless of edges
- Add Edge: O(1) - Direct array access
- Check Edge Exists: O(1) - Direct lookup at matrix[u][v]
- Get All Neighbors: O(V) - Must scan entire row
- Best For: Dense graphs (E ≈ V²), frequent edge lookups

ADJACENCY LIST:
- Space: O(V + E) - V vertices + E edges stored
- Add Edge: O(1) - Append to list
- Check Edge Exists: O(degree of vertex) - Must search list
- Get All Neighbors: O(degree of vertex) - Iterate neighbors only
- Best For: Sparse graphs (most real-world graphs), BFS/DFS traversals

FANG INTERVIEW TIP: ~95% of problems use Adjacency List!
"""

def adjacencyMatrixUndirected(vertice: int, edges: List[List[int]]):
    """
    Build undirected graph using adjacency matrix.

    Time Complexity: O(V² + E)
        - O(V²) to initialize V×V matrix with zeros
        - O(E) to populate edges (2 assignments per edge)

    Space Complexity: O(V²)
        - Matrix always uses V×V space

    Args:
        vertice: Number of vertices (0 to vertice-1)
        edges: List of [u, v] edges
    """
    matrix = [[0]*vertice for _ in range(vertice)]  # O(V²) time & space
    for edge in edges:  # O(E) iterations
        u = edge[0]
        v  = edge[1]
        matrix[u][v] = 1  # O(1) - bidirectional for undirected
        matrix[v][u] = 1  # O(1)
    print(matrix)

def adjacencyMatrixDirected(vertice: int, edges: List[List[int]]):
    """
    Build directed graph using adjacency matrix.

    Time Complexity: O(V² + E)
        - O(V²) to initialize matrix
        - O(E) to add edges (1 assignment per edge)

    Space Complexity: O(V²)

    Args:
        vertice: Number of vertices
        edges: List of [u, v] directed edges (u → v)
    """
    matrix = [[0]*vertice for _ in range(vertice)]  # O(V²)
    for edge in edges:  # O(E)
        u = edge[0]
        v  = edge[1]
        matrix[u][v] = 1  # O(1) - only one direction
    print(matrix)

def adjacencyListUndirected(vertice: int, edges: List[List[int]]):
    """
    Build undirected graph using adjacency list.

    ⚠️ WARNING: This implementation has a BUG!
    Line: adjList = [[]*vertice for _ in range(vertice)]
    This creates a list of references to the SAME empty list.
    Should be: adjList = [[] for _ in range(vertice)]

    Time Complexity: O(V + E) [if bug fixed]
        - O(V) to initialize V empty lists
        - O(E) to append edges (2 appends per edge)
        - List append is amortized O(1)

    Space Complexity: O(V + E)
        - V lists + 2E total elements (each edge stored twice)

    Args:
        vertice: Number of vertices
        edges: List of [u, v] edges
    """
    adjList = [[]*vertice for _ in range(vertice)]  # 🐛 BUG: All same reference!
    for edge in edges:  # O(E)
        u = edge[0]
        v = edge[1]
        adjList[u].append(v)  # Amortized O(1)
        adjList[v].append(u)  # Amortized O(1)
    print(adjList)

def adjacencyListDirected(vertice: int, edges: List[List[int]]):
    """
    Build directed graph using adjacency list.

    ⚠️ WARNING: Same bug as undirected version!

    Time Complexity: O(V + E) [if bug fixed]
        - O(V) to initialize V empty lists
        - O(E) to append edges (1 append per edge)

    Space Complexity: O(V + E)
        - V lists + E elements

    Args:
        vertice: Number of vertices
        edges: List of [u, v] directed edges (u → v)
    """
    adjList = [[]*vertice for _ in range(vertice)]  # 🐛 BUG: All same reference!
    for edge in edges:  # O(E)
        u = edge[0]
        v = edge[1]
        adjList[u].append(v)  # Amortized O(1) - only one direction
    print(adjList)

# ✅ BEST PRACTICE: Use defaultdict for Adjacency List (FANG Interview Standard)

from collections import defaultdict

def adjacencyListDirectedDict(verticeLen: int, edges: List[List[int]], isWeighted = True, isDirected = True):
    """
    Build graph using defaultdict - RECOMMENDED for interviews!

    Time Complexity: O(E) or O(V + E) depending on initialization
        - O(E) to process edges
        - defaultdict creates keys on-demand (no upfront V initialization needed)
        - If you need to ensure all V vertices exist: add O(V) initialization loop

    Space Complexity: O(V + E)
        - Dictionary with V keys
        - Weighted: 2E tuples (undirected) or E tuples (directed)
        - Unweighted: 2E integers (undirected) or E integers (directed)

    Advantages over list-based:
        1. No need to know vertex count upfront
        2. Handles sparse graphs efficiently (no wasted space)
        3. No index out of bounds errors
        4. Cleaner code with automatic key creation
        5. Easy to handle non-integer vertex IDs (strings, etc.)

    Python Internals:
        - defaultdict is a dict subclass with __missing__ method
        - dict in Python 3.7+ maintains insertion order
        - Average case O(1) for key access (hash table)
        - List append is amortized O(1) due to dynamic array resizing

    Args:
        verticeLen: Number of vertices (can be 0 if unknown)
        edges: List of [u, v] or [u, v, weight]
        isWeighted: If True, stores (neighbor, weight) tuples
        isDirected: If False, adds reverse edges

    Returns:
        defaultdict where graph[u] = list of neighbors or (neighbor, weight) tuples

    Example:
        edges = [[0, 1, 10], [1, 2, 20]]
        Weighted directed: {0: [(1, 10)], 1: [(2, 20)]}
        Weighted undirected: {0: [(1, 10)], 1: [(0, 10), (2, 20)], 2: [(1, 20)]}
    """
    graph = defaultdict(list)  # O(1) creation

    if verticeLen == 0 or not edges:  # O(1) edge case check
        return graph

    for edge in edges:  # O(E) iterations
        u, v = edge[0], edge[1]  # O(1) tuple unpacking
        weight = edge[2] if isWeighted and len(edge) > 2 else 1  # O(1)

        if isWeighted:
            graph[u].append((v, weight))  # Amortized O(1)
            if not isDirected:
                graph[v].append((u, weight))  # Amortized O(1)
        else:
            graph[u].append(v)  # Amortized O(1)
            if not isDirected:
                graph[v].append(u)  # Amortized O(1)

    return graph

    

def main():
    """
    Test all graph representations.

    Overall Complexity for this main function:
        - Each representation builds from same edge list
        - Total: O(V² + E) due to matrix initialization dominating
    """
    edges = [[1, 0], [1, 2], [2, 0]]  # 3 vertices (0, 1, 2), 3 edges

    print("=== Adjacency List (Directed) - O(V+E) ===")
    adjacencyListDirected(3, edges)

    print("\n=== Adjacency List (Undirected) - O(V+E) ===")
    adjacencyListUndirected(3, edges)

    print("\n=== Adjacency Matrix (Directed) - O(V²+E) ===")
    adjacencyMatrixDirected(3, edges)

    print("\n=== Adjacency Matrix (Undirected) - O(V²+E) ===")
    adjacencyMatrixUndirected(3, edges)

    print("\n=== defaultdict (Best Practice) - O(E) ===")
    print(adjacencyListDirectedDict(3, edges, isWeighted=False, isDirected=True))

main()

"""
COMPLEXITY COMPARISON SUMMARY FOR FANG INTERVIEWS:

Operation            | Adj Matrix | Adj List (dict) | When to Use
---------------------|------------|-----------------|---------------------------
Space                | O(V²)      | O(V + E)        | List: E << V²
Add Edge             | O(1)       | O(1)            | Tie
Remove Edge          | O(1)       | O(E)            | Matrix: frequent deletions
Check if Edge Exists | O(1)       | O(degree)       | Matrix: frequent queries
Iterate Neighbors    | O(V)       | O(degree)       | List: sparse graphs
BFS/DFS              | O(V²)      | O(V + E)        | List: almost always better

REAL INTERVIEW SCENARIOS:
- Social Network (sparse): Use Adjacency List → O(V+E) << O(V²)
- Complete Graph (dense): Use Matrix if edge queries dominate
- Unknown Vertices: Use defaultdict (can add vertices dynamically)
- Weighted Graphs: defaultdict with tuples → graph[u] = [(v1, w1), (v2, w2)]

PYTHON MEMORY INTERNALS:
- list: Dynamic array, 8 bytes per pointer + object overhead
- dict: Hash table, ~3x memory of list but O(1) lookup
- Matrix: V² * 8 bytes (for integers)
- List: V * (40 bytes list overhead) + E * 8 bytes

For V=1000, E=5000:
- Matrix: ~8 MB
- List: ~80 KB (100x better!)
"""
