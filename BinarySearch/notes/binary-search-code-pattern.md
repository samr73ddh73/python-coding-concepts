# Binary Search Code Patterns

## Core Template

```python
def binary_search(nums: List[int], target: int) -> int:
    """Standard binary search - find target or return -1."""
    lo, hi = 0, len(nums) - 1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            lo = mid + 1  # Search right
        else:
            hi = mid - 1  # Search left
    
    return -1  # Not found
```

**Invariant:** `lo <= hi` continues while search space exists

---

## Pattern 1: Lower Bound (First ≥ target)

```python
def lower_bound(nums: List[int], target: int) -> int:
    """First index where nums[i] >= target."""
    lo, hi = 0, len(nums)
    
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid  # Don't skip mid
    
    return lo  # Will be len(nums) if target not found
```

**Key Difference:** `lo < hi` (not `<=`) and `hi = mid` (not `mid - 1`)

---

## Pattern 2: Upper Bound (First > target)

```python
def upper_bound(nums: List[int], target: int) -> int:
    """First index where nums[i] > target."""
    lo, hi = 0, len(nums)
    
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] <= target:  # Note: <=, not <
            lo = mid + 1
        else:
            hi = mid
    
    return lo
```

**Use:** Find insertion point, count occurrences

---

## Pattern 3: Search in Rotated Array

```python
def search_rotated(nums: List[int], target: int) -> int:
    """Find target in rotated sorted array."""
    lo, hi = 0, len(nums) - 1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        
        # Determine which half is sorted
        if nums[lo] <= nums[mid]:  # Left half sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1  # Target in sorted left
            else:
                lo = mid + 1  # Target in right
        else:  # Right half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1  # Target in sorted right
            else:
                hi = mid - 1  # Target in left
    
    return -1
```

**Key Insight:** At least one half is always sorted; use that to navigate

---

## Pattern 4: Peak Element

```python
def find_peak(nums: List[int]) -> int:
    """Find any peak element (nums[i] > nums[i±1])."""
    lo, hi = 0, len(nums) - 1
    
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1  # Peak is to the right (go uphill)
        else:
            hi = mid  # Peak is left or at mid
    
    return lo  # At convergence, lo = peak
```

**Intuition:** Always move toward the uphill direction

---

## Pattern 5: Binary Search on Answer

```python
def min_eating_speed(piles: List[int], h: int) -> int:
    """Find minimum eating speed to finish all piles in h hours."""
    def can_finish(speed: int) -> bool:
        hours = sum((pile + speed - 1) // speed for pile in piles)  # Ceil division
        return hours <= h
    
    lo, hi = 1, max(piles)
    
    while lo < hi:
        mid = (lo + hi) // 2
        if can_finish(mid):
            hi = mid  # Can finish faster, try slower speeds
        else:
            lo = mid + 1  # Too slow, speed up
    
    return lo
```

**Pattern:**
1. Define feasibility function
2. Binary search on answer range
3. Find first value where predicate is true

---

## Pattern 6: Minimum in Rotated Array

```python
def find_min_rotated(nums: List[int]) -> int:
    """Find minimum in rotated sorted array."""
    lo, hi = 0, len(nums) - 1
    
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:  # Min is in right half
            lo = mid + 1
        else:  # Min is in left half (including mid)
            hi = mid
    
    return nums[lo]
```

**Comparison:** Always compare to `nums[hi]` (not `nums[lo]` or `nums[mid]`)

---

## Pattern 7: Find Single Element (in sorted array with duplicates)

```python
def find_single(nums: List[int]) -> int:
    """Find element appearing once; others appear twice."""
    lo, hi = 0, len(nums) - 1
    
    while lo < hi:
        mid = lo + ((hi - lo) // 2)
        if mid % 2 == 1:
            mid -= 1  # Normalize to even index
        
        if nums[mid] == nums[mid + 1]:  # Normal pair
            lo = mid + 2  # Single is in right
        else:  # Pair broken
            hi = mid  # Single is in left or at mid
    
    return nums[lo]
```

**Use Index Parity:** Pairs have specific index patterns before single element

---

## Pattern 8: Search in 2D Matrix

```python
def search_matrix(matrix: List[List[int]], target: int) -> bool:
    """Search in row-wise and column-wise sorted matrix."""
    if not matrix or not matrix[0]:
        return False
    
    # Treat as flat sorted array
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1
    
    while lo <= hi:
        mid = (lo + hi) // 2
        value = matrix[mid // n][mid % n]  # Convert 1D index to 2D
        
        if value == target:
            return True
        elif value < target:
            lo = mid + 1
        else:
            hi = mid - 1
    
    return False
```

**Index Conversion:**
- 1D → 2D: `(row, col) = (idx // cols, idx % cols)`
- 2D → 1D: `idx = row * cols + col`

---

## Common Mistakes ⚠️

| Mistake | Wrong | Right |
|---------|-------|-------|
| **Overflow** | `mid = (lo + hi) // 2` | `mid = lo + (hi - lo) // 2` |
| **Boundary** | `while lo < hi` for exact match | `while lo <= hi` for LC 704 |
| **Update** | `hi = mid` (may loop forever) | `hi = mid - 1` OR `lo < hi` with `hi = mid` |
| **Target check** | After loop in insertion cases | During loop for exact match |
| **Condition** | `if nums[mid] <= target` (wrong direction) | Match problem requirements |
| **Off-by-one** | Forget to handle edge indices | Be careful with `mid - 1`, `mid + 1` |

---

## When to Use Which

```python
# Exact match
if nums[mid] == target:
    return mid  # or lo

# Lower bound (first >= target)
if nums[mid] < target:
    lo = mid + 1
else:
    hi = mid

# Upper bound (first > target)
if nums[mid] <= target:
    lo = mid + 1
else:
    hi = mid

# Rotated/tricky
Compare with one end to determine sorted half
Move toward target direction
```

---

## Complexity Summary

| Variant | Time | Space | Use |
|---------|------|-------|-----|
| Standard | O(log n) | O(1) | Exact match |
| Lower Bound | O(log n) | O(1) | First ≥ target |
| Upper Bound | O(log n) | O(1) | First > target |
| Rotated | O(log n) | O(1) | Rotated array |
| Peak | O(log n) | O(1) | Local maximum |
| On Answer | O(log answer) | O(1) | Optimization |

---

## Interview Checklist 💡

- [ ] Ask: "Is the array sorted?" → Essential for binary search
- [ ] Consider edge case: target not in array
- [ ] Mention overflow fix: `mid = lo + (hi - lo) // 2`
- [ ] Discuss: exact match vs bounds (lower/upper)
- [ ] For rotated: identify sorted half, navigate accordingly
- [ ] For "on answer": define feasibility function clearly
- [ ] Always verify termination: `lo != hi` after loop
