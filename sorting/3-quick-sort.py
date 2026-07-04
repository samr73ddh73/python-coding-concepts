"""
QUICK SORT
==========
Divide-and-conquer algorithm that partitions array around a pivot element,
then recursively sorts the partitions. One of the most efficient sorting
algorithms in practice.

Core Idea:
1. Choose a pivot element
2. Partition: move all smaller elements left, larger elements right
3. Recursively sort left and right partitions
4. Combine (already sorted in-place)

Key Characteristics:
- Time Complexity: O(n log n) average, O(n²) worst case
- Space Complexity: O(log n) average (recursion stack), O(n) worst case
- Stable: No (order of equal elements may change)
- In-place: Yes (not always, depends on implementation)
- Cache-friendly: Yes (good data locality)
"""

import random


# ============================================================================
# APPROACH 1: LOMUTO PARTITION SCHEME
# ============================================================================
def quickSort_lomuto(arr, low=0, high=None):
    """
    Quick sort using Lomuto partition scheme.
    Pivot is placed at the end during partition.

    Args:
        arr: List to sort
        low: Starting index (default 0)
        high: Ending index (default len(arr)-1)

    Returns:
        Sorted list (sorts in-place)
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        # Partition and get pivot index
        pivot_index = partition_lomuto(arr, low, high)

        # Recursively sort left partition
        quickSort_lomuto(arr, low, pivot_index - 1)

        # Recursively sort right partition
        quickSort_lomuto(arr, pivot_index + 1, high)

    return arr


def partition_lomuto(arr, low, high):
    """
    Lomuto partition: last element as pivot.

    Process:
    1. Choose last element as pivot
    2. Maintain index i for elements <= pivot
    3. Traverse array, move smaller elements before pivot
    4. Place pivot at correct position

    Example: [3, 1, 4, 1, 5, 9, 2, 6]
    Pivot = 6
    - Elements <= 6 move left: [3, 1, 4, 1, 5, 2, 6, 9]
    - Pivot at index 6
    """
    pivot = arr[high]  # Choose last element as pivot
    i = low - 1        # Index of smaller element

    # Traverse through all elements, compare with pivot
    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Swap

    # Place pivot in correct position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ============================================================================
# APPROACH 2: HOARE PARTITION SCHEME
# ============================================================================
def quickSort_hoare(arr, low=0, high=None):
    """
    Quick sort using Hoare partition scheme.
    More efficient than Lomuto (fewer swaps).

    Args:
        arr: List to sort
        low: Starting index
        high: Ending index

    Returns:
        Sorted list (sorts in-place)
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_index = partition_hoare(arr, low, high)
        quickSort_hoare(arr, low, pivot_index)
        quickSort_hoare(arr, pivot_index + 1, high)

    return arr


def partition_hoare(arr, low, high):
    """
    Hoare partition: uses two pointers from both ends.

    Process:
    1. Choose middle element as pivot
    2. Use two pointers: left (starts at low), right (starts at high)
    3. Move pointers towards each other
    4. Swap elements that are on wrong side of pivot
    5. Pointers cross when complete

    More efficient: requires fewer swaps than Lomuto
    """
    pivot = arr[(low + high) // 2]  # Middle element as pivot

    while True:
        # Move left pointer until element >= pivot
        while arr[low] < pivot:
            low += 1

        # Move right pointer until element <= pivot
        while arr[high] > pivot:
            high -= 1

        # If pointers crossed, partition complete
        if low >= high:
            return high

        # Swap elements at both pointers
        arr[low], arr[high] = arr[high], arr[low]
        low += 1
        high -= 1


# ============================================================================
# APPROACH 3: RANDOM PIVOT SELECTION (Randomized Quick Sort)
# ============================================================================
def quickSort_random(arr, low=0, high=None):
    """
    Quick sort with random pivot selection.
    Prevents worst-case performance on sorted/reverse-sorted data.
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_index = partition_random(arr, low, high)
        quickSort_random(arr, low, pivot_index - 1)
        quickSort_random(arr, pivot_index + 1, high)

    return arr


def partition_random(arr, low, high):
    """Random pivot partition: choose pivot randomly."""
    # Pick random index and swap with last element
    random_index = random.randint(low, high)
    arr[random_index], arr[high] = arr[high], arr[random_index]

    # Now use Lomuto partition
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# ============================================================================
# APPROACH 4: 3-WAY PARTITION (Handles Duplicates Efficiently)
# ============================================================================
def quickSort_3way(arr, low=0, high=None):
    """
    3-way quicksort: Divides into 3 parts (less, equal, greater).
    Efficient for arrays with many duplicate elements.

    Partitions:
    - Elements < pivot (left)
    - Elements == pivot (middle) - ALREADY SORTED
    - Elements > pivot (right)

    Then recursively sort left and right (skip middle).
    """
    if high is None:
        high = len(arr) - 1

    if low < high:
        # Returns indices: lt (partition for <) and gt (partition for >)
        lt, gt = partition_3way(arr, low, high)

        # Recursively sort left partition (< pivot)
        quickSort_3way(arr, low, lt - 1)

        # Recursively sort right partition (> pivot)
        quickSort_3way(arr, gt + 1, high)

    return arr


def partition_3way(arr, low, high):
    """
    3-way partition using Dutch National Flag algorithm.

    Returns: (lt, gt)
    - arr[low...lt-1]: elements < pivot
    - arr[lt...gt]: elements == pivot
    - arr[gt+1...high]: elements > pivot
    """
    pivot = arr[low]
    lt = low          # arr[low...lt-1] < pivot
    i = low + 1       # arr[lt...i-1] == pivot
    gt = high         # arr[gt+1...high] > pivot

    while i <= gt:
        if arr[i] < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif arr[i] > pivot:
            arr[i], arr[gt] = arr[gt], arr[i]
            gt -= 1
        else:  # arr[i] == pivot
            i += 1

    return lt, gt


# ============================================================================
# APPROACH 5: ITERATIVE QUICK SORT (Using Stack)
# ============================================================================
def quickSort_iterative(arr):
    """
    Iterative quick sort using explicit stack.
    Avoids recursion overhead and stack overflow on very large arrays.
    """
    if len(arr) <= 1:
        return arr

    # Create stack and push initial low/high
    stack = [(0, len(arr) - 1)]

    while stack:
        low, high = stack.pop()

        if low < high:
            # Partition and get pivot index
            pivot_index = partition_lomuto(arr, low, high)

            # Push left partition
            if low < pivot_index - 1:
                stack.append((low, pivot_index - 1))

            # Push right partition
            if pivot_index + 1 < high:
                stack.append((pivot_index + 1, high))

    return arr


# ============================================================================
# APPROACH 6: HYBRID - INTRO SORT (Introsort)
# ============================================================================
def quickSort_intro(arr, low=0, high=None, depth_limit=None):
    """
    Introsort (Introspective Sort): Hybrid algorithm.

    Strategy:
    1. Start with quick sort
    2. If recursion depth exceeds limit → switch to heap sort
    3. Prevents O(n²) worst case

    Used in: C++ STL std::sort, Java Arrays.sort()
    """
    if high is None:
        high = len(arr) - 1

    if depth_limit is None:
        depth_limit = 2 * len(arr).bit_length()  # Log-based depth limit

    if low < high:
        if depth_limit == 0:
            # Recursion too deep, switch to heap sort
            heapSort_inplace(arr, low, high)
        else:
            pivot_index = partition_lomuto(arr, low, high)
            quickSort_intro(arr, low, pivot_index - 1, depth_limit - 1)
            quickSort_intro(arr, pivot_index + 1, high, depth_limit - 1)

    return arr


def heapSort_inplace(arr, low, high):
    """Simple heap sort for intro sort fallback."""
    def heapify(n, i):
        smallest = i
        left, right = 2 * i + 1, 2 * i + 2
        if left < n and arr[low + left] < arr[low + smallest]:
            smallest = left
        if right < n and arr[low + right] < arr[low + smallest]:
            smallest = right
        if smallest != i:
            arr[low + i], arr[low + smallest] = arr[low + smallest], arr[low + i]
            heapify(n, smallest)

    n = high - low + 1
    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[low], arr[low + i] = arr[low + i], arr[low]
        heapify(i, 0)


# ============================================================================
# VISUALIZATION & EXAMPLES
# ============================================================================
def quickSort_verbose(arr, low=0, high=None, depth=0):
    """Quick sort with step-by-step visualization."""
    if high is None:
        high = len(arr) - 1

    if low < high:
        indent = "  " * depth
        print(f"{indent}Sorting arr[{low}...{high}] = {arr[low:high+1]}")

        pivot_index = partition_lomuto(arr, low, high)
        print(f"{indent}Partition at index {pivot_index}, pivot = {arr[pivot_index]}")
        print(f"{indent}Array after partition: {arr}")

        quickSort_verbose(arr, low, pivot_index - 1, depth + 1)
        quickSort_verbose(arr, pivot_index + 1, high, depth + 1)

    return arr


# ============================================================================
# EXAMPLES
# ============================================================================
def example_basic():
    """Basic quick sort example."""
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("Original:", arr)
    result = quickSort_lomuto(arr.copy())
    print("Sorted:  ", result)
    # Output: [11, 12, 22, 25, 34, 64, 90]


def example_comparison():
    """Compare different partition schemes."""
    arr = [64, 34, 25, 12, 22, 11, 90]

    arr1 = arr.copy()
    quickSort_lomuto(arr1)
    print("Lomuto:  ", arr1)

    arr2 = arr.copy()
    quickSort_hoare(arr2)
    print("Hoare:   ", arr2)

    arr3 = arr.copy()
    quickSort_random(arr3)
    print("Random:  ", arr3)


def example_duplicates():
    """3-way sort efficient with duplicates."""
    arr = [5, 2, 5, 1, 5, 9, 5, 2]
    print("Original:", arr)
    result = quickSort_3way(arr.copy())
    print("3-way:   ", result)


def example_visualization():
    """Step-by-step visualization."""
    arr = [5, 2, 8, 1, 9]
    print("Visualizing quick sort:\n")
    quickSort_verbose(arr)
    print("\nFinal:", arr)


def example_iterative():
    """Iterative quick sort."""
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("Iterative:", quickSort_iterative(arr.copy()))


# ============================================================================
# COMPLEXITY ANALYSIS
# ============================================================================
"""
TIME COMPLEXITY:
================
Best Case: O(n log n)
  - When pivot divides array evenly
  - Tree depth = log(n), each level does O(n) work
  - Example: 1,000,000 elements = ~20 levels

Average Case: O(n log n)
  - With random or good pivots
  - Slightly higher constant than merge sort
  - Practical fastest sorting algorithm

Worst Case: O(n²)
  - When pivot is always smallest/largest
  - Array: [1, 2, 3, 4, 5, 6, 7, 8]
  - Pivot always at end = n + (n-1) + (n-2) + ... = n²/2
  - Solution: Use random pivot, 3-way partition, or hybrid

SPACE COMPLEXITY:
=================
Best/Average Case: O(log n)
  - Recursion stack depth = log(n) on average
  - Each recursive call uses constant space

Worst Case: O(n)
  - Stack depth can reach n (linear tree)
  - Use iterative approach to save space

COMPARISONS & SWAPS:
====================
Average: ~2n ln(n) comparisons, ~n ln(n)/6 swaps
Better swap ratio than merge sort (fewer copies)
"""


# ============================================================================
# PERFORMANCE COMPARISON
# ============================================================================
"""
Algorithm       | Best       | Average    | Worst      | Space    | Stable
Insertion Sort  | O(n)       | O(n²)      | O(n²)      | O(1)     | Yes
Selection Sort  | O(n²)      | O(n²)      | O(n²)      | O(1)     | No
Bubble Sort     | O(n)       | O(n²)      | O(n²)      | O(1)     | Yes
Merge Sort      | O(n log n) | O(n log n) | O(n log n) | O(n)     | Yes
Quick Sort      | O(n log n) | O(n log n) | O(n²)      | O(log n) | No
Heap Sort       | O(n log n) | O(n log n) | O(n log n) | O(1)     | No
Intro Sort      | O(n log n) | O(n log n) | O(n log n) | O(log n) | No

Why Quick Sort is Popular:
✓ O(n log n) average - faster than merge sort in practice
✓ O(log n) space - much better than merge sort's O(n)
✓ Cache-friendly - sequential data access
✓ In-place - no extra array allocation
✗ Not stable - equal elements may reorder
✗ Worst-case O(n²) - need good pivot strategy
"""


# ============================================================================
# USE CASES OF QUICK SORT
# ============================================================================
"""
1. GENERAL-PURPOSE SORTING ⭐⭐⭐⭐⭐
   - Default choice for most applications
   - Fast average case O(n log n) with good constants
   - Used in most programming language libraries (C++, Java, Python)
   - Example: Sorting user data, database records

2. EXTERNAL SORTING
   - Divide-and-conquer naturally works with limited memory
   - Can process data larger than RAM
   - Example: Sorting billion-row datasets on disk

3. REAL-TIME SYSTEMS
   - Average O(n log n) acceptable
   - Use randomized pivot to avoid worst case
   - Introsort guarantees O(n log n) always
   - Example: Embedded systems, trading systems

4. LARGE DATASETS
   - Space-efficient: O(log n) vs O(n) for merge sort
   - Fast in practice despite theoretical complexity
   - Excellent cache locality
   - Example: Sorting multi-GB files

5. IN-PLACE SORTING REQUIRED
   - Need minimal extra memory
   - Can't allocate extra O(n) array
   - Example: Sorting arrays on memory-constrained devices

6. ONLINE PARTIAL SORTING
   - Can find k-th smallest/largest element efficiently
   - Partition finds exact position
   - O(n) average using select algorithm (variation)
   - Example: Finding top-10 records from million records

7. ARRAYS WITH MANY DUPLICATES
   - Use 3-way partitioning
   - Equal elements already in final position
   - Avoid redundant sorting
   - Example: Sorting records with many duplicate values

8. CACHE-FRIENDLY SORTING
   - Sequential data access pattern
   - Better CPU cache utilization
   - Fewer memory misses than other O(n log n) sorts
   - Example: High-performance computing, data analytics

9. MULTI-KEY SORTING
   - Recursively sort by different keys
   - Combine with other sorts for specific properties
   - Example: Sort by dept, then by salary, then by name

10. HYBRID ALGORITHMS (Introsort)
    - Default in C++ STL (std::sort)
    - Default in Java (Arrays.sort for primitives)
    - Quick sort + heap sort fallback
    - Guarantees O(n log n) worst case
"""


# ============================================================================
# WHEN NOT TO USE QUICK SORT
# ============================================================================
"""
❌ Worst Case Scenarios:

1. STABILITY REQUIRED
   - Must preserve order of equal elements
   - Use: Merge sort or timsort
   - Example: Maintaining database row order

2. GUARANTEED O(n log n) REQUIRED
   - Real-time systems with strict latency requirements
   - Use: Merge sort, heap sort, or introsort
   - Example: Streaming video codec, flight control

3. NEARLY SORTED DATA
   - Insertion sort approaches O(n)
   - Quick sort still O(n log n)
   - Example: Real-time monitoring data with small updates

4. VERY SMALL ARRAYS (n < 10)
   - Overhead of recursion not worth it
   - Use: Insertion sort directly
   - (Good implementations use hybrid approach)
"""


# ============================================================================
# TIPS FOR OPTIMAL PERFORMANCE
# ============================================================================
"""
Pivot Selection Strategies:
============================
1. RANDOM PIVOT (Best)
   - Avoids worst case on pre-sorted data
   - O(n log n) expected even on sorted input
   - Use for general purpose

2. MEDIAN-OF-THREE
   - Choose median of (first, middle, last)
   - Avoids worst case on sorted data
   - Slightly better than random
   - Use when random not available

3. MEDIAN-OF-MEDIANS
   - Guarantees O(n log n) in worst case
   - Higher constant factors
   - Rarely used in practice

4. FIRST/LAST ELEMENT
   - Simple but bad for sorted data
   - Avoid for general purpose

Optimization Techniques:
========================
1. SWITCH TO INSERTION SORT for small subarrays (n < 10-20)
2. USE 3-WAY PARTITION for data with many duplicates
3. USE ITERATIVE with stack to avoid recursion overhead
4. USE INTROSORT (hybrid) for guaranteed performance
5. CACHE-OPTIMIZE by reducing memory access patterns
"""


# ============================================================================
# PRACTICE PROBLEMS
# ============================================================================
"""
Recommended Problems:

1. Basic Sorting
   - Sort array using quick sort

2. Variations
   - Sort in descending order
   - Sort by custom comparator
   - Sort specific data type (strings, tuples, objects)

3. Advanced
   - K-th smallest/largest element (using partition)
   - Count inversions while sorting
   - Sort colors (3-way partition) - LeetCode 75
   - Wiggle sort (alternate high-low)

4. Hybrid Problems
   - Median of data stream (heap + quick sort concepts)
   - Top K frequent elements
   - Sort almost sorted array
"""


if __name__ == "__main__":
    print("=" * 70)
    print("QUICK SORT - COMPREHENSIVE GUIDE")
    print("=" * 70)

    print("\n1. BASIC EXAMPLE:")
    example_basic()

    print("\n2. PARTITION SCHEME COMPARISON:")
    example_comparison()

    print("\n3. WITH DUPLICATES (3-way partition):")
    example_duplicates()

    print("\n4. VISUALIZATION (Step by Step):")
    example_visualization()

    print("\n5. ITERATIVE APPROACH:")
    example_iterative()