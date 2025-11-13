
from typing import Deque, Set, List, Dict
from collections import defaultdict, deque

"""
BFS WITHOUT DEQUE - COMPLEXITY ANALYSIS

This file demonstrates different queue implementations for BFS and their
performance implications. CRITICAL for FANG interviews!
"""

# ============================================================
# METHOD 1: Using deque (BEST - Always use this!)
# ============================================================

def bfs_with_deque(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    Standard BFS using collections.deque.

    Time Complexity: O(V + E)
        - V vertices visited once
        - E edges processed once
        - popleft() is O(1)
        - append() is O(1)

    Space Complexity: O(V)
        - Queue: O(V)
        - Visited: O(V)

    ✅ ALWAYS USE THIS IN INTERVIEWS!
    """
    if not graph:
        return []

    result = []
    visited = set()
    visited.add(start)
    queue = deque([start])  # Double-ended queue

    while queue:
        node = queue.popleft()  # O(1) - removes from left end
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)  # O(1) - adds to right end

    return result


# ============================================================
# METHOD 2: Using list with pop(0) - SLOW! ❌
# ============================================================

def bfs_with_list_pop0(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    BFS using list with pop(0) - INEFFICIENT!

    Time Complexity: O(V² + E) ❌ WORSE THAN O(V + E)!
        - V vertices visited
        - E edges processed
        - pop(0) is O(n) because it shifts all remaining elements left!
        - If queue has k elements, pop(0) takes O(k) time
        - Total for all pops: O(V²) in worst case

    Space Complexity: O(V)

    Why pop(0) is O(n):
        list = [a, b, c, d, e]
        list.pop(0)  # Returns 'a'
        # Now list = [b, c, d, e]
        # Python had to shift b→0, c→1, d→2, e→3
        # That's O(n) work!

    ❌ NEVER USE THIS! It's a common beginner mistake.
    """
    if not graph:
        return []

    result = []
    visited = set()
    visited.add(start)
    queue = [start]  # Regular list

    while queue:
        node = queue.pop(0)  # ❌ O(n) - shifts all elements!
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)  # O(1) - amortized

    return result


# ============================================================
# METHOD 3: Using list with index pointer - SMART! ✅
# ============================================================

def bfs_with_list_index(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    BFS using list with index pointer - Good alternative to deque!

    Time Complexity: O(V + E) ✅ SAME AS DEQUE!
        - No shifting needed
        - Just increment index pointer
        - Trade-off: doesn't free memory as we go

    Space Complexity: O(V)
        - Slightly worse than deque (doesn't free processed elements)
        - Queue grows to V elements and stays there

    How it works:
        queue = [0, 1, 2, 3, 4]
        idx   =  ^  (process 0, increment idx)
        idx   =     ^  (process 1, increment idx)
        # Elements before idx are "logically removed" but still in memory

    ✅ Acceptable in interviews if you can't remember deque!
    """
    if not graph:
        return []

    result = []
    visited = set()
    visited.add(start)
    queue = [start]
    idx = 0  # Points to current element to process

    while idx < len(queue):  # While there are unprocessed elements
        node = queue[idx]  # O(1) - just read at index
        idx += 1  # O(1) - move pointer forward
        result.append(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)  # O(1) - amortized

    return result


# ============================================================
# METHOD 4: Using two lists (level by level) - READABLE! ✅
# ============================================================

def bfs_with_two_lists(graph: Dict[int, List[int]], start: int) -> List[int]:
    """
    BFS using two lists - processes level by level.

    Time Complexity: O(V + E) ✅
        - Each vertex processed once
        - Each edge checked once
        - No shifting needed

    Space Complexity: O(V)
        - Two lists, but max combined size is O(V)

    Advantages:
        - Very readable
        - Natural for level-order problems
        - No deque import needed

    ✅ Good for explaining BFS concepts in interviews!
    """
    if not graph:
        return []

    result = []
    visited = set()
    visited.add(start)
    current_level = [start]  # Current level to process

    while current_level:
        next_level = []  # Build next level

        for node in current_level:  # Process entire current level
            result.append(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    next_level.append(neighbor)

        current_level = next_level  # Move to next level

    return result


# ============================================================
# PERFORMANCE COMPARISON
# ============================================================

def compare_performance():
    """
    Demonstrates performance difference between methods.
    """
    import time

    # Build larger test graph
    graph = defaultdict(list)
    n = 1000  # 1000 vertices

    # Create a graph: 0→1→2→...→999 (linear chain)
    for i in range(n - 1):
        graph[i].append(i + 1)

    print("=== PERFORMANCE COMPARISON (1000 vertices) ===\n")

    # Method 1: deque
    start = time.perf_counter()
    result1 = bfs_with_deque(graph, 0)
    time1 = time.perf_counter() - start
    print(f"1. deque.popleft():     {time1*1000:.3f}ms ✅ FASTEST")

    # Method 2: list.pop(0) - SLOWEST
    start = time.perf_counter()
    result2 = bfs_with_list_pop0(graph, 0)
    time2 = time.perf_counter() - start
    print(f"2. list.pop(0):         {time2*1000:.3f}ms ❌ SLOWEST ({time2/time1:.1f}x slower)")

    # Method 3: list with index
    start = time.perf_counter()
    result3 = bfs_with_list_index(graph, 0)
    time3 = time.perf_counter() - start
    print(f"3. list with index:     {time3*1000:.3f}ms ✅ Good")

    # Method 4: two lists
    start = time.perf_counter()
    result4 = bfs_with_two_lists(graph, 0)
    time4 = time.perf_counter() - start
    print(f"4. two lists:           {time4*1000:.3f}ms ✅ Good")

    print(f"\nAll methods returned same result: {result1 == result2 == result3 == result4}")


# ============================================================
# PYTHON INTERNALS DEEP DIVE
# ============================================================

"""
WHY IS pop(0) SLOW?

Python list internals:
- Lists are dynamic arrays stored contiguously in memory
- Memory layout: [item0, item1, item2, item3, ...]
                  ^
                  Pointer to start

When you call pop(0):
1. Remove item at index 0
2. Shift item1 to index 0
3. Shift item2 to index 1
4. Shift item3 to index 2
5. ... shift all remaining elements

Example with 5 elements:
    Before: [A, B, C, D, E]
             0  1  2  3  4

    pop(0) → returns A

    After:  [B, C, D, E, _]  (4 shifts!)
             0  1  2  3  4

    Then list shrinks: [B, C, D, E]
                        0  1  2  3

This is O(n) where n = len(list)!

-------------------------

WHY IS deque FAST?

collections.deque internals:
- Implemented as doubly-linked list of blocks
- Each block contains ~62 pointers to actual elements
- Can add/remove from both ends efficiently

Structure:
    HEAD ←→ [block1] ←→ [block2] ←→ [block3] ←→ TAIL
            [items]     [items]     [items]

popleft():
1. Remove from HEAD block
2. If block empty, remove block
3. No shifting needed!

This is O(1)!

-------------------------

MEMORY COMPARISON:

list:
- More memory efficient for storage
- Each element: 8 bytes (pointer)
- Overhead: ~56 bytes + capacity buffer

deque:
- Slightly more memory per element
- Block overhead: ~512 bytes per block
- Each element: 8 bytes + block structure

For BFS with 1000 vertices:
- list: ~8 KB
- deque: ~10 KB
- Difference: Negligible!

Performance gain from O(1) popleft far outweighs memory cost!
"""

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

    print("=== Testing All BFS Implementations ===\n")

    print("1. BFS with deque (BEST):")
    print(f"   Result: {bfs_with_deque(graph, 0)}")

    print("\n2. BFS with list.pop(0) (SLOW):")
    print(f"   Result: {bfs_with_list_pop0(graph, 0)}")

    print("\n3. BFS with list + index (GOOD):")
    print(f"   Result: {bfs_with_list_index(graph, 0)}")

    print("\n4. BFS with two lists (GOOD):")
    print(f"   Result: {bfs_with_two_lists(graph, 0)}")

    print("\n" + "="*60)
    compare_performance()


if __name__ == "__main__":
    run_tests()


"""
==================== FANG INTERVIEW SUMMARY ====================

QUESTION: "Can I do BFS without deque?"
ANSWER: Yes, but complexity changes!

┌─────────────────┬──────────────┬────────────┬──────────────┐
│ Method          │ Time         │ Space      │ Interview?   │
├─────────────────┼──────────────┼────────────┼──────────────┤
│ deque           │ O(V + E)     │ O(V)       │ ✅ BEST      │
│ list.pop(0)     │ O(V² + E) ❌ │ O(V)       │ ❌ NEVER     │
│ list + index    │ O(V + E)     │ O(V)*      │ ✅ OK        │
│ two lists       │ O(V + E)     │ O(V)       │ ✅ OK        │
└─────────────────┴──────────────┴────────────┴──────────────┘

*Slightly higher space (doesn't free processed elements)

==================== INTERVIEWER FOLLOW-UPS ====================

Q: "Why not just use list.pop(0)?"
A: "pop(0) is O(n) because Python lists are dynamic arrays that need
    to shift all remaining elements left. This degrades BFS from
    O(V+E) to O(V²+E). For a graph with 1000 vertices, that's
    1000x slower!"

Q: "What if the interviewer says no imports allowed?"
A: "I'd use the list with index pointer approach. It maintains O(V+E)
    time complexity by avoiding the shift operation. The trade-off is
    we don't free memory as we go, but that's acceptable."

Q: "How does deque achieve O(1) popleft?"
A: "deque is implemented as a doubly-linked list of blocks, not a
    contiguous array. Removing from either end just updates pointers,
    no shifting needed."

==================== RELATED LEETCODE PATTERNS ====================

1. Standard BFS: Use deque
   - Binary Tree Level Order (102)
   - Rotting Oranges (994)
   - Word Ladder (127)

2. Level-order processing: Use two lists OR deque with size
   - Binary Tree Zigzag (103)
   - N-ary Tree Level Order (429)

3. When interviewer restricts imports: Use list + index
   - Mention the complexity trade-offs!

==================== REMEMBER ====================

⚠️  CRITICAL MISTAKE: Using list.pop(0) in BFS
    - Seen in ~30% of junior candidates
    - Automatic red flag in FANG interviews
    - Always use deque or explain alternatives!

✅ SHOW YOU KNOW: Mention why you're using deque
    - "I'm using deque for O(1) popleft operations"
    - Shows you understand data structure trade-offs
    - Separates you from candidates who just memorize
"""

