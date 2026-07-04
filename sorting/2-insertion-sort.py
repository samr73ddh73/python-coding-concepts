"""
INSERTION SORT
==============
Builds the sorted array one item at a time by comparing each element
with already-sorted elements and inserting it at the correct position.

How it works:
1. Start with the second element (index 1)
2. Compare it with elements before it (sorted portion)
3. Shift larger elements one position right
4. Insert the current element in its correct position
5. Repeat until all elements are processed

Key Characteristics:
- Time Complexity: O(n²) average & worst case, O(n) best case
- Space Complexity: O(1) - in-place sorting
- Stable: Yes (maintains relative order of equal elements)
- Online: Yes (can sort as it receives data)
- Adaptive: Yes (efficient on nearly-sorted data)
"""



def insertionSort(arr):
    """
    Sorts array in-place using insertion sort algorithm.

    Args:
        arr: List of comparable elements

    Returns:
        Sorted list (modifies in-place)
    """
    # Start from second element (index 1)
    for i in range(1, len(arr)):
        key = arr[i]  # Element to be inserted
        j = i - 1     # Index of last element in sorted portion

        # Compare with sorted portion and shift larger elements right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]  # Shift right
            j -= 1

        # Insert key at correct position
        arr[j + 1] = key

    return arr


# ============================================================================
# EXAMPLE 1: Basic usage
# ============================================================================
def example_basic():
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("Original:", arr)
    result = insertionSort(arr.copy())
    print("Sorted:  ", result)
    # Output: [11, 12, 22, 25, 34, 64, 90]

# ============================================================================
# EXAMPLE 3: Different data types
# ============================================================================
def example_strings():
    """Insertion sort works with any comparable data."""
    words = ["zebra", "apple", "mango", "banana"]
    print("Original:", words)
    result = insertionSort(words.copy())
    print("Sorted:  ", result)
    # Output: ['apple', 'banana', 'mango', 'zebra']


def example_tuples():
    """Sort tuples by first element (natural comparison)."""
    pairs = [(3, 'c'), (1, 'a'), (2, 'b')]
    print("Original:", pairs)
    result = insertionSort(pairs.copy())
    print("Sorted:  ", result)
    # Output: [(1, 'a'), (2, 'b'), (3, 'c')]


# ============================================================================
# EXAMPLE 4: Descending order
# ============================================================================
def insertionSort_descending(arr):
    """Sort in descending order."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # Change comparison: use < instead of >
        while j >= 0 and arr[j] < key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr


def example_descending():
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("Descending:", insertionSort_descending(arr.copy()))


# ============================================================================
# EXAMPLE 5: Binary insertion sort (optimization)
# ============================================================================
def insertionSort_binary(arr):
    """
    Use binary search to find insertion position (faster comparisons).
    Note: Still O(n²) due to shifting, but reduces comparison overhead.
    """
    from bisect import bisect_left

    for i in range(1, len(arr)):
        key = arr[i]
        # Find position using binary search
        pos = bisect_left(arr, key, 0, i)

        # Shift elements
        arr = arr[:pos] + [key] + arr[pos:i] + arr[i+1:]

    return arr


def example_binary():
    arr = [64, 34, 25, 12, 22, 11, 90]
    print("Binary insertion sort:", insertionSort_binary(arr.copy()))


# ============================================================================
# COMPLEXITY ANALYSIS
# ============================================================================
"""
TIME COMPLEXITY:
================
Best Case: O(n)
  - When array is already sorted
  - Inner while loop never executes
  - Only 1 comparison per element

Average Case: O(n²)
  - Each element compared with ~n/2 previous elements
  - n × n/2 = n²/2 comparisons

Worst Case: O(n²)
  - When array is reverse sorted
  - Each element compared with all previous elements
  - Total: 1 + 2 + 3 + ... + (n-1) = n(n-1)/2 comparisons

SPACE COMPLEXITY:
=================
O(1) - Only uses constant extra space (in-place sorting)

COMPARISONS & SWAPS:
====================
Best Case:    n-1 comparisons, 0 swaps
Average Case: ~n²/4 comparisons, ~n²/4 swaps
Worst Case:   ~n²/2 comparisons, ~n²/2 swaps
"""


# ============================================================================
# USE CASES
# ============================================================================
"""
1. NEARLY SORTED DATA ⭐⭐⭐⭐⭐
   - Time complexity approaches O(n) for nearly sorted data
   - Use when most elements are already in order
   - Example: Real-time data streams with small changes

2. SMALL ARRAYS
   - Low overhead makes it faster than quicksort/mergesort for n < 50
   - Practical threshold varies by implementation
   - Example: Sorting small subarrays in hybrid algorithms

3. HYBRID ALGORITHMS
   - Timsort (Python's built-in) uses insertion sort on small runs
   - Used in Introsort as base case
   - Combines with divide-and-conquer for larger data

4. ONLINE SORTING
   - Can sort elements as they arrive (streaming data)
   - No need to have entire dataset upfront
   - Example: Sorting incoming sensor readings in real-time

5. MEMORY CONSTRAINED SYSTEMS
   - O(1) space complexity is crucial
   - No recursion needed (no stack overhead)
   - Example: Embedded systems, IoT devices

6. STABLE SORT REQUIRED
   - Maintains relative order of equal elements
   - Important in multi-key sorting
   - Example: Sort by last name, then by first name

7. CACHE FRIENDLY (for small n)
   - Sequential access pattern is cache-friendly
   - Better than quicksort for small arrays

8. ADAPTIVE SORTING
   - Performance depends on input order
   - Can detect and exploit partial order
   - Example: Adaptive algorithms for real-world data
"""


# ============================================================================
# COMPARISON WITH OTHER SORTS
# ============================================================================
"""
Algorithm       | Best   | Average | Worst  | Space  | Stable | Online
----------      |--------|---------|--------|--------|--------|--------
Insertion Sort  | O(n)   | O(n²)   | O(n²)  | O(1)   | Yes    | Yes
Selection Sort  | O(n²)  | O(n²)   | O(n²)  | O(1)   | No     | No
Bubble Sort     | O(n)   | O(n²)   | O(n²)  | O(1)   | Yes    | Yes
Merge Sort      | O(n log n)         | O(n log n)  | O(n)   | Yes    | No
Quick Sort      | O(n log n)         | O(n²)  | O(log n)| No    | No
Heap Sort       | O(n log n)         | O(n log n)  | O(1)   | No     | No

When to use Insertion Sort:
✓ n < 50 (small arrays)
✓ Nearly sorted data
✓ Memory limited
✓ Need stable sort + O(1) space
✓ Online/streaming sorting
✗ Large random datasets (use quicksort/mergesort)
"""


# ============================================================================
# PRACTICE PROBLEMS
# ============================================================================
def insertion_sort_practice():
    """
    Recommended problems to practice insertion sort concepts:

    1. Sort an array using insertion sort (basic)
    2. Sort array in descending order
    3. Sort array of objects by specific property
    4. Count inversions while sorting (variation)
    5. Sort nearly-sorted array efficiently
    6. Implement binary insertion sort
    7. Online sorting of streaming data
    """
    pass


if __name__ == "__main__":
    print("=" * 70)
    print("INSERTION SORT EXAMPLES")
    print("=" * 70)

    print("\n1. Basic Example:")
    example_basic()

    print("\n2. Visualization (Step by Step):")
    example_visualization()

    print("\n3. String Sorting:")
    example_strings()

    print("\n4. Tuple Sorting:")
    example_tuples()

    print("\n5. Descending Order:")
    example_descending()

    print("\n6. Binary Insertion Sort:")
    example_binary()
