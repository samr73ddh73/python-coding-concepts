def bubble_sort(arr):
    """
    Bubble Sort: Compares adjacent elements and swaps if out of order.
    Larger elements "bubble" to the end of the array.
    """
    n = len(arr)

    for i in range(n - 1):
        swapped = False
        # Each pass, compare adjacent elements
        # Reduce range by i since last i elements are sorted
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:  # Compare adjacent elements
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        # Optimization: if no swaps, array is sorted
        if not swapped:
            return arr

    return arr


def selection_sort(arr):
    """
    Selection Sort: Finds minimum element in remaining array
    and places it at current position.
    """
    n = len(arr)

    for i in range(n - 1):
        # Find minimum element from i to end
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j

        # Swap minimum with current position
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr


# Test both
arr1 = [10, 21, 3, 4, 5]
arr2 = [10, 21, 3, 4, 5]

print(f"Original: {[10, 21, 3, 4, 5]}")
print(f"Bubble Sort: {bubble_sort(arr1)}")
print(f"Selection Sort: {selection_sort(arr2)}")

# Time Complexity:
# Bubble Sort:
#   - Best: O(n) - if already sorted (with optimization)
#   - Average: O(n²)
#   - Worst: O(n²)
#   - Space: O(1) - in-place
#   - Stable: Yes
#
# Selection Sort:
#   - Best: O(n²) - always, no optimization possible
#   - Average: O(n²)
#   - Worst: O(n²)
#   - Space: O(1) - in-place
#   - Stable: No (depends on implementation)
