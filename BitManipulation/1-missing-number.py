# Missing Number via XOR
# Core Insight
# XOR has two key properties:

# a ^ a = 0 (same numbers cancel out)
# a ^ 0 = a (XOR with zero is identity)

# So if you XOR a number with itself, it disappears. If every index i is XORed with nums[i], all present numbers cancel — leaving only the missing one.
# Walkthrough
# nums = [3, 0, 1]   →  n = 3, missing = 2

# XOR all indices:  0 ^ 1 ^ 2 ^ 3
# XOR all values:   3 ^ 0 ^ 1

# Combined: 0 ^ 1 ^ 2 ^ 3 ^ 3 ^ 0 ^ 1
#         = (0^0) ^ (1^1) ^ (3^3) ^ 2
#         = 0 ^ 0 ^ 0 ^ 2
#         = 2  ✓

def missingNumber(nums):
    xor = len(nums)
    for i, n in enumerate(nums):
        xor = xor ^ i ^ n
    return xor