import math
class Solution:
    def mirrorDistance(self, n: int) -> int:
        rev = self.reverse(n)
        return abs(n-rev)

    def reverse(self, n: int):
        dig = int(math.log10(n))
        print(dig)
        new = 0
        while(n > 0):
            unit = n%10
            new = unit* pow(10, dig) + new
            n = n//10
            dig = dig -1
        print(new)
        return new


# The issue is likely that `log(n, 10)` in Python can give floating-point precision errors, causing incorrect results when you cast to int.

# Here's what's happening:

# ```python
# import math

# n = 1000
# digits = int(math.log(n, 10)) + 1
# print(digits)  # Expected: 4, but might get 3!
# ```

# The problem: `log(1000, 10)` should be exactly `3.0`, but due to floating-point arithmetic, it might be `2.9999999999999996`, and `int()` truncates it to `2`.

# **Solution: Use floor with a small epsilon OR use log10:**

# ```python
# import math

# # Method 1: Using log10 (more accurate for base 10)
# def count_digits(n):
#     if n == 0:
#         return 1
#     return int(math.log10(abs(n))) + 1

# # Method 2: Adding small epsilon to handle precision
# def count_digits_safe(n):
#     if n == 0:
#         return 1
#     return int(math.log10(abs(n)) + 1e-9) + 1

# # Method 3: Most robust - handle edge case with floor
# def count_digits_robust(n):
#     if n == 0:
#         return 1
#     return math.floor(math.log10(abs(n))) + 1
# ```

# **Test cases:**
# ```python
# test_cases = [1, 10, 100, 1000, 9999, 10000, 999999]
# for n in test_cases:
#     print(f"{n}: {count_digits(n)} digits")
# ```

# **Why `log10` is better than `log(n, 10)`:**
# - `math.log10()` is optimized for base-10 and has better precision
# - `math.log(n, 10)` does `ln(n) / ln(10)` which compounds rounding errors

# Which scenario are you hitting this issue with? Powers of 10 specifically?