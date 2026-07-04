## https://leetcode.com/problems/single-number-ii/

### How to Recognize a Bitwise Approach

# Ask yourself these questions when you see an array problem:


# 1. Does the problem involve numbers appearing a fixed number of times?
# 2. Is there a "leftover" element that breaks the pattern?
# 3. Are you asked for O(1) space with O(n) time?
# ```

# The key signal is **"everything appears K times except one"** — this screams bit counting, because:
# - Each bit position is **independent**
# - If every number appeared K times, every bit position's sum would be **divisible by K**
# - The leftover bits (sum % K) reconstruct the answer



## Approach 1 — O(32) Space: Count Bits Mod 3

### Idea

# Look at each of the 32 bit positions independently. Count how many numbers have a `1` in that position. If the count is **not divisible by 3**, the single number has a `1` there.

# ```
# nums = [2, 2, 3, 2]

# Bit pos 1:  2→1, 2→1, 3→1, 2→1  → sum=4, 4%3 = 1  → single number has 1 here
# Bit pos 0:  2→0, 2→0, 3→1, 2→0  → sum=1, 1%3 = 1  → single number has 1 here

# Reconstruct: bit1=1, bit0=1  →  11 in binary = 3  ✓
# ```

### Code

def singleNumber(nums: list[int]) -> int:
    result = 0
    for bit in range(32):
        bit_sum = 0
        for num in nums:
            bit_sum += (num >> bit) & 1   # extract this bit from every number
        
        remainder = bit_sum % 3           # leftover belongs to single number
        result |= remainder << bit        # place it back in the right position
    
    return result


### Why This Works Visually


# bit position:     2   1   0

# num=2  (010):     0   1   0
# num=2  (010):     0   1   0
# num=3  (011):     0   1   1
# num=2  (010):     0   1   0
#                ─────────────
# col sum:          0   4   1
#       % 3:        0   1   1   →  011 = 3 ✓

# Each column is completely independent — the triplets always contribute a multiple of 3, so they vanish under mod 3.

# **Complexity:** Time O(32·n), Space O(1) — the array of 32 counts is constant size, but conceptually it's "heavier" than the ones-twos trick.


