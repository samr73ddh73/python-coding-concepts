"""
ROTATED SORTED ARRAY - QUICK REVISION

WHAT IS A ROTATED SORTED ARRAY?
================================
Original sorted: [1, 2, 3, 4, 5, 6, 7]
Rotated at pivot 4: [5, 6, 7, 1, 2, 3, 4]
                     ↑pivot point

Key property: Array is split into TWO sorted subarrays
- Left part: [5, 6, 7] - sorted
- Right part: [1, 2, 3, 4] - sorted
- Pivot: Where rotation happened (smallest element)

WITHOUT DUPLICATES: Time = O(log n)
===================================
Binary search works perfectly because:
- You can ALWAYS identify which half is sorted
- If nums[mid] >= nums[left] → left half is sorted
- Else → right half is sorted

Example: [4,5,6,7,0,1,2], target=0
         L     M     R
- nums[M]=7 >= nums[L]=4 → left sorted
- target=0 not in [4,7] → search right
- Guaranteed O(log n)

WITH DUPLICATES: Worst Case = O(n) ❌
=========================================
THE PROBLEM: Can't determine which half is sorted!

Example: [1,1,1,1,1,1,1,1,2,1,1,1,1], target=2
          L         M         R

nums[L] = nums[M] = nums[R] = 1

Question: Which half is sorted?
- Left half: [1,1,1,1,1,1,1] - Could be sorted OR rotated!
- Right half: [1,1,1,1,1,1,1] - Could be sorted OR rotated!
- Answer: IMPOSSIBLE TO TELL! 😱

WHY THIS BREAKS BINARY SEARCH:
==============================
Binary search relies on ELIMINATING half the search space each time.
With duplicates where nums[L] == nums[M] == nums[R]:
- Can't determine sorted half
- Can't safely eliminate either half
- Must check BOTH sides → degrades to O(n)

THE FIX (Line 13-15):
=====================
if nums[start] == nums[mid] == nums[end]:
    start += 1  # Skip left boundary
    end -= 1    # Skip right boundary

This removes duplicates from boundaries, but:
- Worst case: All elements are same except one
  Example: [1,1,1,1,1,2,1,1,1,1,1]
- Must shrink by 1 each time → O(n) worst case

TIME COMPLEXITY:
================
Best case: O(log n) - No duplicates or few duplicates
Worst case: O(n) - All elements same (e.g., [1,1,1,1,2,1,1,1])
Average case: O(log n) to O(n) depending on duplicate density

SPACE COMPLEXITY: O(1)

VISUAL EXAMPLE - THE DUPLICATE PROBLEM:
========================================
Array: [2,2,2,3,2,2,2]
         L   M   R

nums[L]=2, nums[M]=3, nums[R]=2
- Wait, nums[M] != nums[L] and nums[M] != nums[R]
- This case is fine! Can determine sorted half.

Array: [2,2,2,2,2,2,3]
         L     M   R

nums[L]=2, nums[M]=2, nums[R]=3
- Can determine right is sorted (nums[M] <= nums[R])
- This works!

Array: [2,2,2,2,2,2,2]
         L     M   R

nums[L]=2, nums[M]=2, nums[R]=2
- STUCK! Can't determine ANYTHING
- Target could be hidden anywhere
- Must linear search → O(n)

KEY INSIGHT:
============
Duplicates break the "one half is always sorted" invariant
that makes binary search work in rotated arrays.

When boundaries equal mid, we lose the ability to:
1. Identify which half is sorted
2. Eliminate half the search space
3. Maintain O(log n) complexity

INTERVIEW TIP:
==============
Always clarify: "Does the array contain duplicates?"
- No duplicates → Guaranteed O(log n)
- With duplicates → Mention worst case O(n)
"""

from typing import List

# Worst case example: [1,1,1,1,1,1,1,1,2]

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        start, end = 0, len(nums)-1
        while(start <= end):
            mid = (start+end)//2
            if nums[mid] == target:
                return True
            if nums[start] == nums[mid] == nums[end]:
                start += 1
                end -= 1
            elif nums[mid]<= nums[start] and nums[mid]<= nums[end]: #right is sorted and left is not
                if target >= nums[mid] and target <= nums[end]:
                    start = mid+1
                else:
                    end = mid -1
            elif nums[mid] >= nums[start] and nums[mid] >= nums[end]:
                if target <= nums[mid] and target >= nums[start]:
                    end = mid-1
                else:
                    start = mid+1
            elif nums[mid] >= nums[start] and nums[mid] <= nums[end]:
                if target <= nums[mid]:
                    end = mid-1
                else:
                    start = mid+1
        return False
    
def main():
    ans = Solution().search([1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1,1,1], 2)
    print(ans)

main()