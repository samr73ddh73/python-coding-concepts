"""
================================================================================
PATTERN: Prime Number Algorithms
================================================================================

DEFINITION: A prime number is divisible only by 1 and itself (n > 1)

Examples: 2, 3, 5, 7, 11, 13, 17, 19, 23...
Not Prime: 1 (by definition), 4, 6, 8, 9, 10...

KEY OPTIMIZATIONS:
1. Only check divisors up to n (not n)
2. Skip even numbers after checking 2
3. Use Sieve of Eratosthenes for finding all primes up to N
"""

import math

# ============================================================================
# METHOD 1: Basic Approach - O(n)
# ============================================================================
def is_prime_basic(n: int) -> bool:
    """
    Check if n is prime by testing all divisors from 2 to n-1
    TIME: O(n) - SLOW for large n
    """
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:  # Even numbers (except 2) are not prime
        return False

    for i in range(3, n, 2):  # Check odd divisors
        if n % i == 0:
            return False
    return True


# ============================================================================
# METHOD 2: Optimized Approach - O(n)  BEST for single check
# ============================================================================
def is_prime(n: int) -> bool:
    """
    Check if n is prime by testing divisors up to n

    KEY INSIGHT: If n = a * b, then either a d n or b d n
    So we only need to check divisors up to n!

    TIME: O(n)
    SPACE: O(1)

    Example: n = 36
    - 36 = 6
    - Divisors: 1×36, 2×18, 3×12, 4×9, 6×6
    - Notice: After 6, divisors just swap (9×4, 12×3, etc.)
    - So checking up to 6 is enough!
    """
    if n <= 1:
        return False
    if n <= 3:
        return True  # 2 and 3 are prime
    if n % 2 == 0 or n % 3 == 0:
        return False  # Divisible by 2 or 3

    # Check divisors of form 6k ± 1 up to n
    # Why? All primes > 3 are of form 6k±1
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


# ============================================================================
# METHOD 3: Sieve of Eratosthenes - O(n log log n)  BEST for finding ALL primes
# ============================================================================
def sieve_of_eratosthenes(n: int) -> list[int]:
    """
    Find all prime numbers up to n using Sieve of Eratosthenes

    ALGORITHM:
    1. Create array [2, 3, 4, ..., n]
    2. For each prime p, mark all multiples of p as composite
    3. Remaining unmarked numbers are prime

    TIME: O(n log log n) - very efficient!
    SPACE: O(n)

    Use this when you need to find MANY primes up to N
    """
    if n < 2:
        return []

    # Create boolean array, True = prime
    is_prime_arr = [True] * (n + 1)
    is_prime_arr[0] = is_prime_arr[1] = False  # 0 and 1 are not prime

    # Start from 2, mark all multiples as composite
    p = 2
    while p * p <= n:
        if is_prime_arr[p]:
            # Mark all multiples of p as composite
            for i in range(p * p, n + 1, p):
                is_prime_arr[i] = False
        p += 1

    # Collect all primes
    return [i for i in range(n + 1) if is_prime_arr[i]]


"""
SIEVE TRACE: Find primes up to 30

Initial: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

p=2: Mark 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30
     [2, 3, X, 5, X, 7, X, 9, X, 11, X, 13, X, 15, X, 17, X, 19, X, 21, X, 23, X, 25, X, 27, X, 29, X]

p=3: Mark 9, 15, 21, 27 (6, 12, 18, 24, 30 already marked)
     [2, 3, X, 5, X, 7, X, X, X, 11, X, 13, X, X, X, 17, X, 19, X, X, X, 23, X, 25, X, X, X, 29, X]

p=5: Mark 25 (10, 15, 20 already marked)
     [2, 3, X, 5, X, 7, X, X, X, 11, X, 13, X, X, X, 17, X, 19, X, X, X, 23, X, X, X, X, X, 29, X]

p=7: 7*7=49 > 30, STOP

Primes: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] 
"""


# ============================================================================
# METHOD 4: Count Primes up to N (LeetCode style)
# ============================================================================
def count_primes(n: int) -> int:
    """
    Count how many prime numbers are less than n

    TIME: O(n log log n)
    SPACE: O(n)
    """
    if n <= 2:
        return 0

    is_prime_arr = [True] * n
    is_prime_arr[0] = is_prime_arr[1] = False

    for i in range(2, int(n**0.5) + 1):
        if is_prime_arr[i]:
            for j in range(i*i, n, i):
                is_prime_arr[j] = False

    return sum(is_prime_arr)


# ============================================================================
# METHOD 5: Find Nth Prime Number
# ============================================================================
def nth_prime(n: int) -> int:
    """
    Find the nth prime number (1-indexed)

    Example: nth_prime(6) = 13
    Primes: 2, 3, 5, 7, 11, 13
              1  2  3  4  5   6
    """
    if n == 1:
        return 2

    count = 1  # Already counted 2
    candidate = 3

    while count < n:
        if is_prime(candidate):
            count += 1
        candidate += 2  # Skip even numbers

    return candidate - 2


# ============================================================================
# METHOD 6: Prime Factorization
# ============================================================================
def prime_factorization(n: int) -> list[int]:
    """
    Find all prime factors of n

    Example: 60 = 2 × 2 × 3 × 5
    Returns: [2, 2, 3, 5]

    TIME: O(n)
    """
    factors = []

    # Check for 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # Check odd factors from 3 to n
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2

    # If n > 1, then it's a prime factor
    if n > 1:
        factors.append(n)

    return factors


"""
EXAMPLES & TESTS
"""

if __name__ == '__main__':
    print("=== Single Prime Check ===")
    print(f"is_prime(17): {is_prime(17)}")  # True
    print(f"is_prime(18): {is_prime(18)}")  # False
    print(f"is_prime(97): {is_prime(97)}")  # True

    print("\n=== All Primes up to N ===")
    print(f"Primes up to 30: {sieve_of_eratosthenes(30)}")

    print("\n=== Count Primes ===")
    print(f"Count primes < 20: {count_primes(20)}")  # 8 primes: 2,3,5,7,11,13,17,19

    print("\n=== Nth Prime ===")
    print(f"6th prime: {nth_prime(6)}")  # 13
    print(f"10th prime: {nth_prime(10)}")  # 29

    print("\n=== Prime Factorization ===")
    print(f"Factors of 60: {prime_factorization(60)}")  # [2, 2, 3, 5]
    print(f"Factors of 84: {prime_factorization(84)}")  # [2, 2, 3, 7]
    print(f"Factors of 17: {prime_factorization(17)}")  # [17] (prime itself)


"""
================================================================================
FANG INTERVIEW POINTS:
================================================================================

1. "Check divisors up to n, not n - huge optimization!"

2. "Skip even numbers after checking 2"

3. "For finding single prime: O(n) is optimal"

4. "For finding ALL primes up to N: Use Sieve O(n log log n)"

5. "Primes > 3 are of form 6k±1 (6k-1 or 6k+1)"

6. "Sieve starts marking from p² because smaller multiples already marked"

================================================================================
COMPLEXITY COMPARISON:
================================================================================

Task                    | Best Algorithm        | Time          | Space
------------------------|-----------------------|---------------|--------
Check if N is prime     | Optimized Trial Div   | O(n)         | O(1)
Find all primes d N     | Sieve of Eratosthenes | O(n log log n)| O(n)
Count primes < N        | Sieve of Eratosthenes | O(n log log n)| O(n)
Prime factorization     | Trial Division        | O(n)         | O(log n)
Find Nth prime          | Trial Division + Loop | O(nn)        | O(1)

================================================================================
COMMON MISTAKES:
================================================================================

L for i in range(2, n):  ’ O(n), too slow!
 for i in range(2, int(n**0.5) + 1):  ’ O(n)

L Forgetting n d 1 returns False
 if n <= 1: return False

L Not handling n = 2 separately
 if n == 2: return True

L Checking all numbers in sieve
 Only check up to n, mark from p²
"""
