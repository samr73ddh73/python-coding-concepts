# Two-Pointer Pattern

## Core Concept
- Use two pointers traversing from **different directions or speeds**
- Solve problems in-place with **O(1) extra space**
- Common in: sorted arrays, linked lists, strings

## When to Use
✓ Remove/move elements in-place  
✓ Palindrome checking  
✓ Container with most water  
✓ Trapping rain water  
✓ Sliding window on sorted array  
✓ Find pair with target sum  
✓ Merge sorted arrays  

---

## Pattern 1: Same Direction (Slow & Fast)

```python
def remove_duplicates(nums: List[int]) -> int:
    """Remove duplicates from sorted array in-place."""
    if not nums:
        return 0
    
    slow = 0  # Boundary of processed section
    
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    
    return slow + 1
```

**Pattern:**
- `slow`: marks next valid position
- `fast`: scans ahead
- When condition met: `slow++`, then update `nums[slow]`

**Problems:** Remove duplicates, Remove element, Move zeroes

---

## Pattern 2: Move Zeros to End

```python
def move_zeros(nums: List[int]) -> None:
    """Move all zeros to end while maintaining order."""
    slow = 0
    
    # First, move all non-zeros to front
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow] = nums[fast]
            slow += 1
    
    # Fill rest with zeros
    while slow < len(nums):
        nums[slow] = 0
        slow += 1
```

**Variation:** Instead of final fill, can swap:
```python
for fast in range(len(nums)):
    if nums[fast] != 0:
        nums[slow], nums[fast] = nums[fast], nums[slow]
        slow += 1
```

---

## Pattern 3: Opposite Directions (Left & Right)

```python
def two_sum_sorted(nums: List[int], target: int) -> List[int]:
    """Find two numbers that sum to target (1-indexed)."""
    left, right = 0, len(nums) - 1
    
    while left < right:
        current_sum = nums[left] + nums[right]
        
        if current_sum == target:
            return [left + 1, right + 1]  # 1-indexed
        elif current_sum < target:
            left += 1  # Need larger sum
        else:
            right -= 1  # Need smaller sum
    
    return []  # No solution
```

**Key Insight:** 
- If sorted array: move pointers toward middle
- left++/right-- based on comparison with target

---

## Pattern 4: Palindrome Check

```python
def is_palindrome(s: str) -> bool:
    """Check if string is palindrome (ignoring spaces & case)."""
    left, right = 0, len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        # Compare
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True
```

**Pattern:** Skip invalid characters, compare valid ones

---

## Pattern 5: Reverse String/Array In-Place

```python
def reverse_string(s: List[str]) -> None:
    """Reverse list in-place."""
    left, right = 0, len(s) - 1
    
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
```

**Note:** Check if `left < right` (not `<=`) to avoid middle swap

---

## Pattern 6: Container with Most Water

```python
def max_area(height: List[int]) -> int:
    """Find two lines that form container with most water."""
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        # Area = width × min(height)
        width = right - left
        current_area = width * min(height[left], height[right])
        max_area = max(max_area, current_area)
        
        # Move pointer at shorter height (might find taller)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area
```

**Greedy Logic:** Always move the shorter line inward (other is bottleneck)

---

## Pattern 7: Merge Sorted Arrays

```python
def merge(nums1: List[int], m: int, nums2: List[int], n: int) -> None:
    """Merge nums2 into nums1 in-place."""
    # Work backwards to avoid overwriting
    p1, p2, p = m - 1, n - 1, m + n - 1
    
    while p1 >= 0 and p2 >= 0:
        if nums1[p1] > nums2[p2]:
            nums1[p] = nums1[p1]
            p1 -= 1
        else:
            nums1[p] = nums2[p2]
            p2 -= 1
        p -= 1
    
    # If nums2 remains, copy it (nums1 leftovers already in place)
    while p2 >= 0:
        nums1[p] = nums2[p2]
        p2 -= 1
        p -= 1
```

**Key:** Start from **end** to avoid overwriting; leftover from nums2 needs copy only

---

## Pattern 8: 3Sum / K-Sum

```python
def three_sum(nums: List[int]) -> List[List[int]]:
    """Find all triplets that sum to zero."""
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue  # Skip duplicates
        
        target = -nums[i]
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            current_sum = nums[left] + nums[right]
            
            if current_sum == target:
                result.append([nums[i], nums[left], nums[right]])
                
                # Skip duplicate pairs
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < target:
                left += 1
            else:
                right -= 1
    
    return result
```

**Pattern:** Sort first, use two-pointer for target sum, skip duplicates

---

## Pattern 9: Sliding Window with Pointers

```python
def max_sliding_window(nums: List[int], k: int) -> List[int]:
    """Maximum element in each sliding window of size k."""
    left, right = 0, 0
    result = []
    
    while right < len(nums):
        # Expand window
        if right - left + 1 < k:
            right += 1
        else:
            # Window size == k, compute
            window_max = max(nums[left:right + 1])
            result.append(window_max)
            left += 1
            right += 1
    
    return result
```

**Better with deque:** Maintains monotonic deque for O(n) instead of O(nk)

---

## Pattern 10: Remove N-th Node from End

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def remove_nth_from_end(head: ListNode, n: int) -> ListNode:
    """Remove n-th node from end of linked list."""
    dummy = ListNode(0)
    dummy.next = head
    
    fast, slow = dummy, dummy
    
    # Advance fast by n+1
    for _ in range(n + 1):
        if not fast:
            return head  # n is larger than list
        fast = fast.next
    
    # Move both until fast is None
    while fast:
        fast = fast.next
        slow = slow.next
    
    # Remove node
    slow.next = slow.next.next
    return dummy.next
```

**Gap Technique:** fast ahead by n+1, so slow lands at node before target

---

## Common Pitfalls ⚠️

| Pitfall | Wrong | Right |
|---------|-------|-------|
| **Boundary** | `while left <= right` | `while left < right` (prevent overlap) |
| **Update slow in loop** | Update slow anywhere | Update after assignment |
| **Swap vs Assignment** | Forget swap in two-pointer | Use swap for correct logic |
| **Duplicate handling** | Don't skip | Use while loop to skip all duplicates |
| **Backward merge** | Merge from start | Merge from end to avoid overwrite |
| **Linked list gap** | n positions gap | Use n+1 gap to land **before** target |

---

## Complexity Summary

| Variant | Time | Space | Use |
|---------|------|-------|-----|
| Same direction | O(n) | O(1) | Remove, move elements |
| Opposite | O(n) | O(1) | Sum pairs, palindrome |
| Palindrome | O(n) | O(1) | Validation |
| Container | O(n) | O(1) | Max area |
| Merge | O(m+n) | O(1) | In-place merge |
| 3Sum | O(n²) | O(1) | Multiple sums |
| Sliding Window | O(n) or O(nk) | O(1) | Window problems |
| Remove Nth | O(n) | O(1) | Linked list |

---

## Interview Tips 💡

1. **In-place requirement**: Two-pointer is your answer
2. **Sorted array**: Consider two-pointer from opposite ends
3. **Slow-fast pattern**: Good for modify-in-place problems
4. **Duplicate handling**: Always skip duplicates in result
5. **Backward operations**: Safer for in-place modifications
6. **Gap technique**: Use for finding node before target
7. **Early termination**: Check boundary conditions (pointer validity)
8. **Space optimization**: Mention O(1) space improvement over alternatives
