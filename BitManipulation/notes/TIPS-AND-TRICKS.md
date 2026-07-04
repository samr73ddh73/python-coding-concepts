# 🎯 Bit Manipulation Tips & Tricks

> Essential bit operations and patterns for solving bit manipulation problems

---

## Core Operations

### Basic Bit Operations

```python
a & b      # AND: both bits 1
a | b      # OR: at least one 1
a ^ b      # XOR: different bits are 1
~a         # NOT: flip all bits
a << n     # Left shift: multiply by 2^n
a >> n     # Right shift: divide by 2^n
```

---

## Key Properties & Tricks

### XOR Properties (Game Changer!)

**Property 1: Same numbers cancel out**
```python
a ^ a = 0
```

**Property 2: XOR with 0 preserves**
```python
a ^ 0 = a
```

**Property 3: Commutative and Associative**
```python
a ^ b ^ a = b  # Order doesn't matter
```

**Use Case: Find single element**
```python
# All elements appear twice except one
def findSingle(nums):
    result = 0
    for num in nums:
        result ^= num  # Same elements cancel, single survives
    return result
```

---

## Common Patterns

### Pattern 1: Check/Set/Clear Bits

```python
# Check if ith bit is set
def isBitSet(num, i):
    return (num >> i) & 1

# Set ith bit
def setBit(num, i):
    return num | (1 << i)

# Clear ith bit
def clearBit(num, i):
    return num & ~(1 << i)

# Toggle ith bit
def toggleBit(num, i):
    return num ^ (1 << i)
```

### Pattern 2: Count Set Bits

```python
# Brian Kernighan's Algorithm - O(k) where k is number of set bits
def countSetBits(num):
    count = 0
    while num:
        num &= num - 1  # Remove rightmost set bit
        count += 1
    return count

# Python built-in
bin(num).count('1')  # Count '1's in binary representation
```

### Pattern 3: Power of Two Check

```python
# n & (n-1) == 0 means n is power of 2
def isPowerOfTwo(n):
    return n > 0 and (n & (n - 1)) == 0
```

**Why it works:** Power of 2 has only 1 bit set. n-1 flips all bits after that bit, so AND gives 0.

### Pattern 4: Get All Subsets (Bit Enumeration)

```python
def getAllSubsets(nums):
    n = len(nums)
    subsets = []
    for mask in range(1 << n):  # 2^n possibilities
        subset = []
        for i in range(n):
            if mask & (1 << i):  # Check if ith bit set
                subset.append(nums[i])
        subsets.append(subset)
    return subsets
```

---

## Key Insights

### "Everything appears K times except one"

**Signal:** This screams bit counting because bits are independent!

```python
# Example: Everything appears 3 times except one
def findSingle(nums):
    # Count bits at each position
    bit_counts = [0] * 32
    for num in nums:
        for i in range(32):
            bit_counts[i] += (num >> i) & 1
    
    # Result is bits that don't divide evenly by 3
    result = 0
    for i in range(32):
        if bit_counts[i] % 3:
            result |= (1 << i)
    return result
```

### Missing Number Pattern

```python
# Find missing number 0 to n
def findMissing(nums):
    # XOR all numbers and all indices
    # Missing number survives
    result = 0
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result ^ len(nums)
```

---

## Time & Space Complexity

| Operation | Time | Notes |
|---|---|---|
| Single bit check | O(1) | Constant |
| Set/Clear/Toggle bit | O(1) | Constant |
| Count set bits | O(k) | k = number of set bits |
| Brian Kernighan | O(k) | Better than O(32) |
| Bit enumeration | O(2^n · n) | For all subsets |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forget negative numbers | Use 32-bit or handle separately |
| Wrong bit indexing | 0-indexed from right |
| Overflow in shifts | Check language limits |
| XOR with wrong operands | Make sure logic is correct |
| Not handling zero | Special case when needed |

---

## Patterns by Problem Type

### Find Single Element
- All appear twice except one → XOR
- All appear k times except one → Count bits modulo k

### Power of Two
- Check power: `n & (n-1) == 0`
- Next power: Find rightmost set bit

### Subsets
- Bit enumeration: Loop mask 0 to 2^n - 1
- Each bit determines inclusion

### Number Properties
- Even/Odd: `n & 1`
- Rightmost set bit: `n & -n`
- Clear rightmost set bit: `n & (n-1)`

---

## Interview Tips

1. **XOR is your friend:** Cancels equal elements
2. **Bit indexing:** 0 is rightmost, increases left
3. **Powers of 2:** `n & (n-1)` is magic for power checks
4. **Subsets:** Use bitmask enumeration
5. **Shifting:** Left shift = multiply, right shift = divide
6. **Complexity:** Mention O(1) for bit operations
7. **Edge cases:** Zero, negative numbers, overflow

---

## Quick Reference

```python
# Common operations
(num >> i) & 1           # Get ith bit
num | (1 << i)           # Set ith bit
num & ~(1 << i)          # Clear ith bit
num ^ (1 << i)           # Toggle ith bit
num & (num - 1)          # Clear rightmost set bit
num & -num               # Get rightmost set bit (isolate)
n & (n - 1) == 0         # Check if power of 2
bin(num).count('1')      # Count set bits
1 << n                   # 2^n
```

---

*Tips for bit manipulation problems in interviews*
