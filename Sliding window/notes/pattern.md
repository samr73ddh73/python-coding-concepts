<!-- TSliding WIndow Technique:
1. Constant Window Size
2. Dynamic Size


template:

for end in range(n):
    //shrink size:
    while(condition invalid):
        start++
    
    //accept current element or process current element in window
    sum += nums[end]
        
    //check window condition:
    if windowConditionMet:
        processFinal result -->



# Kadane's Algorithm

## Core Concept
Kadane's algorithm finds the **maximum sum of a contiguous subarray** in O(n) time.

**Key Insight:** At each position, decide: should we extend the previous subarray or start fresh?
- If `current_sum < 0`, it's better to start fresh (reset to current element)
- Otherwise, extend the subarray by adding the current element

## Pattern

```python
def maxSubArray(nums):
    max_sum = current_sum = nums[0]
    
    for i in range(1, len(nums)):
        # Either extend previous subarray or start fresh
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum
```

## Variants

### 1. Track the subarray indices
```python
def maxSubArrayWithIndices(nums):
    max_sum = nums[0]
    current_sum = nums[0]
    start = end = 0
    temp_start = 0
    
    for i in range(1, len(nums)):
        if nums[i] > current_sum + nums[i]:
            current_sum = nums[i]
            temp_start = i
        else:
            current_sum += nums[i]
        
        if current_sum > max_sum:
            max_sum = current_sum
            start = temp_start
            end = i
    
    return max_sum, (start, end)
```

### 2. Maximum product subarray
```python
def maxProduct(nums):
    max_prod = min_prod = nums[0]
    result = nums[0]
    
    for i in range(1, len(nums)):
        # Need both max and min because negative * negative = positive
        max_prod, min_prod = (
            max(nums[i], max_prod * nums[i], min_prod * nums[i]),
            min(nums[i], max_prod * nums[i], min_prod * nums[i])
        )
        result = max(result, max_prod)
    
    return result
```

### 3. Maximum circular subarray sum
```python
def maxCircularSubArray(nums):
    # Case 1: Max subarray not wrapping
    max_kadane = maxSubArray(nums)
    
    # Case 2: Max subarray wrapping (total - min subarray)
    total_sum = sum(nums)
    min_kadane = minSubArray(nums)
    max_circular = total_sum - min_kadane
    
    # Edge case: if all negative, return max_kadane
    return max(max_kadane, max_circular) if max_circular != 0 else max_kadane
```

## Why Kadane's Works (DP Perspective)

At each position `i`:
```
max_sum[i] = max(nums[i], max_sum[i-1] + nums[i])
```

- `nums[i]` = start fresh from current element
- `max_sum[i-1] + nums[i]` = extend previous subarray

## Time & Space
- **Time:** O(n) - single pass
- **Space:** O(1) - only tracking current and max sum

---

## Questions & Patterns

### Pattern Questions

**Q1: Maximum Subarray Sum**
- LeetCode 53
- Input: `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`
- Output: `6` (subarray `[4, -1, 2, 1]`)
- Difficulty: Easy

**Q2: Maximum Product Subarray**
- LeetCode 152
- Input: `[2, 3, -2, 4]`
- Output: `6` (subarray `[2, 3]`)
- Note: Handle negatives carefully (negative * negative = positive)
- Difficulty: Medium

**Q3: Maximum Sum of Two Non-Overlapping Subarrays**
- LeetCode 1031
- Given two non-overlapping subarrays of fixed lengths `firstLen` and `secondLen`
- Find maximum sum
- Approach: Precompute max ending at each position, then find best pair
- Difficulty: Medium

**Q4: Circular Array Loop**
- LeetCode 457
- Given circular array of non-zero integers, detect if there's a loop
- Related: Similar to Kadane but with circular logic
- Difficulty: Medium

**Q5: Maximum Subarray Sum with One Deletion**
- LeetCode 1186
- Find max subarray sum after optionally deleting one element
- Approach: Track max ending here and max with one deletion
- Difficulty: Medium

### When to Use Kadane's

✅ **Use when:**
- Finding maximum/minimum sum of **contiguous subarray**
- Subarray length is not fixed
- Need single pass O(n) solution
- Elements can be negative

❌ **Don't use when:**
- Finding max sum of **non-contiguous** elements (use DP or greedy)
- Need indices of all possible subarrays
- Subarray has fixed length (use sliding window instead)

### Common Mistakes

1. **Forgetting to initialize `max_sum`** with first element (not 0)
2. **Not handling all-negative arrays** correctly
3. **Mixing up max_product variant** - must track both max and min
4. **Circular case** - forgetting the edge case where max_circular = 0 (all elements negative)
