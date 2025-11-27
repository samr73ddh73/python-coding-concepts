"""
================================================================================
PATTERN: Fast Exponentiation (Binary Exponentiation)
================================================================================

PROBLEM: Calculate x^n efficiently

NAIVE APPROACH (WRONG - O(n)):
x^4 = x * x * x * x  (4 multiplications)
x^100 = x * x * ... * x  (100 multiplications) ❌ Too slow!

OPTIMIZED APPROACH (CORRECT - O(log n)):
x^4 = (x^2)^2  (2 multiplications: x^2, then square it)
x^100 = (x^50)^2 = ((x^25)^2)^2 = ...  (only log₂(100) ≈ 7 multiplications)

KEY INSIGHT:
x^n = (x^(n/2))^2           if n is even
x^n = x * (x^((n-1)/2))^2   if n is odd

TIME COMPLEXITY: O(log n) - each recursion halves n
SPACE COMPLEXITY: O(log n) - recursion stack depth
"""

def myPow(x: float, n: int) -> float:
    """
    Calculate x^n using fast exponentiation
    Handles negative exponents: x^(-n) = 1 / x^n
    """
    if n == 0:
        return 1.0

    if n < 0:
        return 1.0 / helper(x, -n)

    return helper(x, n)

def helper(x: float, n: int) -> float:
    """
    Fast exponentiation using divide and conquer
    O(log n) time complexity
    """
    # Base case
    if n == 0:
        return 1.0

    # Recursive case: divide n by 2
    half = helper(x, n // 2)

    # If n is even: x^n = (x^(n/2))^2
    if n % 2 == 0:
        return half * half
    # If n is odd: x^n = x * (x^(n/2))^2
    else:
        return x * half * half

"""
EXAMPLE TRACE: myPow(2, 10)

helper(2, 10):
  half = helper(2, 5)
    half = helper(2, 2)
      half = helper(2, 1)
        half = helper(2, 0)
          return 1.0
        n=1 is odd → return 2 * 1 * 1 = 2
      n=2 is even → return 2 * 2 = 4
    n=5 is odd → return 2 * 4 * 4 = 32
  n=10 is even → return 32 * 32 = 1024

Answer: 2^10 = 1024 ✓

Recursion depth: 4 (log₂(10) ≈ 3.3)
Multiplications: 4 (not 10!)

COMPARISON:
Linear approach: 10 multiplications
Binary approach: 4 multiplications ✓
"""

# Alternative: Iterative approach (O(log n) time, O(1) space)
def myPow_iterative(x: float, n: int) -> float:
    """
    Iterative fast exponentiation using bit manipulation
    More space-efficient (no recursion stack)
    """
    if n == 0:
        return 1.0

    if n < 0:
        x = 1 / x
        n = -n

    result = 1.0
    current_product = x

    while n > 0:
        # If current bit is 1, multiply result by current_product
        if n % 2 == 1:
            result *= current_product

        # Square the current_product for next bit
        current_product *= current_product

        # Move to next bit
        n //= 2

    return result

"""
ITERATIVE TRACE: myPow_iterative(2, 10)

Binary of 10: 1010

n=10 (1010), result=1, current=2
  n%2=0 → result=1, current=2*2=4, n=5

n=5 (101), result=1, current=4
  n%2=1 → result=1*4=4, current=4*4=16, n=2

n=2 (10), result=4, current=16
  n%2=0 → result=4, current=16*16=256, n=1

n=1 (1), result=4, current=256
  n%2=1 → result=4*256=1024, current=256*256, n=0

Answer: 1024 ✓

WHY THIS WORKS:
2^10 = 2^(1010 in binary)
     = 2^8 * 2^2
     = 256 * 4
     = 1024
"""

if __name__ == '__main__':
    print(f"Recursive: {myPow(2, 10)}")       # 1024.0
    print(f"Iterative: {myPow_iterative(2, 10)}")  # 1024.0
    print(f"Negative: {myPow(2, -3)}")        # 0.125 (1/8)
    print(f"Zero: {myPow(2, 0)}")             # 1.0

"""
FANG INTERVIEW POINTS:

1. "Naive O(n) is too slow - use binary exponentiation for O(log n)"

2. "Key insight: x^n = (x^(n/2))^2 - halve the problem each time"

3. "Handle odd n by multiplying extra x: x^5 = x * (x^2)^2"

4. "Negative exponent: x^(-n) = 1 / x^n"

5. "Iterative approach uses O(1) space vs O(log n) recursion stack"

6. "Time: O(log n), Space: O(log n) recursive, O(1) iterative"

COMMON MISTAKES:
❌ x = x * helper(x, n-1)  → O(n) linear recursion
✓ half = helper(x, n//2)  → O(log n) divide and conquer
"""
