# Shortest Common Supersequence (SCS)

A comprehensive guide to understanding and implementing the Shortest Common Supersequence problem.

---

## 📖 **Problem Statement**

**Given two strings `s1` and `s2`, find the shortest string that has both `s1` and `s2` as subsequences.**

### Example:
```
s1 = "geek"
s2 = "eke"

SCS = "geeke" (length 5)

Verification:
- "geek" is a subsequence of "geeke": g-e-e-k-e ✓
- "eke" is a subsequence of "geeke": g-e-k-e ✓
```

---

## 🔑 **Key Formula**

```
Length of SCS = len(s1) + len(s2) - len(LCS)
```

### Why This Works:

1. **Total characters needed:** `len(s1) + len(s2)` if no overlap
2. **Characters in LCS:** These appear in BOTH strings
3. **Optimization:** Count LCS characters once instead of twice
4. **Result:** Subtract LCS length from total

### Visual Example:

```
s1 = "AGGTAB" (length 6)
s2 = "GXTXAYB" (length 7)

LCS = "GTAB" (length 4)

SCS length = 6 + 7 - 4 = 9

SCS = "AGXGTXAYB"
  - Contains "AGGTAB": A-G-G-T-A-B
  - Contains "GXTXAYB": G-X-T-X-A-Y-B
```

---

## 🎯 **Algorithm Overview**

### **Two-Step Process:**

1. **Build LCS DP Table** - Standard LCS algorithm
2. **Backtrack to Construct SCS** - Similar to printing LCS, but with a twist

### **Backtracking Logic:**

| Condition | Action | Reason |
|-----------|--------|--------|
| `s1[i-1] == s2[j-1]` | Add char once, move diagonal | Part of LCS - appears in both |
| `dp[i-1][j] > dp[i][j-1]` | Add `s1[i-1]`, move up | Not in LCS - unique to s1 |
| Otherwise | Add `s2[j-1]`, move left | Not in LCS - unique to s2 |

**Key Difference from LCS:**
- **LCS:** Only add when characters match
- **SCS:** Add characters from BOTH strings (matching chars once, non-matching chars from both)

---

## 💻 **Complete Implementation**

```python
from typing import List


def shortest_common_supersequence(s1: str, s2: str) -> str:
    """
    Find shortest common supersequence using LCS approach.

    Time Complexity: O(n × m)
    Space Complexity: O(n × m)

    Args:
        s1, s2: Input strings

    Returns:
        Shortest string containing both s1 and s2 as subsequences

    Example:
        >>> shortest_common_supersequence("geek", "eke")
        'geeke'
    """
    n, m = len(s1), len(s2)

    # Step 1: Build LCS DP table
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Step 2: Backtrack to build SCS
    result = []
    i, j = n, m

    # Process while both strings have characters
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            # Characters match - part of LCS
            # Add once and move diagonally
            result.append(s1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            # LCS comes from above (skip s1[i-1])
            # So s1[i-1] is NOT in LCS - must add it
            result.append(s1[i-1])
            i -= 1
        else:
            # LCS comes from left (skip s2[j-1])
            # So s2[j-1] is NOT in LCS - must add it
            result.append(s2[j-1])
            j -= 1

    # Add remaining characters from s1 (if any)
    while i > 0:
        result.append(s1[i-1])
        i -= 1

    # Add remaining characters from s2 (if any)
    while j > 0:
        result.append(s2[j-1])
        j -= 1

    # Result is built backwards, so reverse
    return ''.join(reversed(result))


def scs_length_only(s1: str, s2: str) -> int:
    """
    Compute only the length of SCS (simpler).
    Uses formula: len(s1) + len(s2) - len(LCS)

    Time: O(n × m)
    Space: O(n × m)
    """
    n, m = len(s1), len(s2)

    # Compute LCS length
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    lcs_length = dp[n][m]
    scs_length = n + m - lcs_length

    return scs_length
```

---

## 🎨 **Step-by-Step Example**

**Input:** `s1 = "geek"`, `s2 = "eke"`

### **Step 1: Build LCS DP Table**

```
       ""  e  k  e
""      0  0  0  0
g       0  0  0  0
e       0  1  1  1
e       0  1  1  2
k       0  1  2  2

LCS length = dp[4][3] = 2
```

The LCS is "ek" (length 2)

### **Step 2: Backtrack to Build SCS**

Starting at `(i=4, j=3)`:

```
Position (4,3): s1[3]='k', s2[2]='e'
  - 'k' ≠ 'e'
  - dp[3][3]=2 > dp[4][2]=2? No (equal)
  - Go LEFT: add s2[2]='e'
  - result = ['e']
  - Move to (4, 2)

Position (4,2): s1[3]='k', s2[1]='k'
  - 'k' == 'k' ✓
  - MATCH: add 'k' once
  - result = ['e', 'k']
  - Move diagonally to (3, 1)

Position (3,1): s1[2]='e', s2[0]='e'
  - 'e' == 'e' ✓
  - MATCH: add 'e' once
  - result = ['e', 'k', 'e']
  - Move diagonally to (2, 0)

Position (2,0): j=0, so add remaining s1
  - Add s1[1]='e': result = ['e', 'k', 'e', 'e']
  - Add s1[0]='g': result = ['e', 'k', 'e', 'e', 'g']
  - Move to (0, 0)

Done! Reverse: ['e', 'k', 'e', 'e', 'g'] → "geeke" ✓
```

### **Verification:**

```
SCS = "geeke"

Is "geek" a subsequence?
  g e e k e
  ↓ ↓ ↓ ↓
  g e e k   ✓

Is "eke" a subsequence?
  g e k e
    ↓ ↓ ↓
    e k e   ✓

Length = 5 = 4 + 3 - 2 ✓
```

---

## 🔍 **Common Mistakes & Fixes**

### **Mistake 1: Wrong Base Cases**

```python
# ❌ WRONG
def scs_wrong(s1, s2, n, m):
    if n == 0:
        return ''  # Missing remaining chars from s2!
    if m == 0:
        return ''  # Missing remaining chars from s1!
```

**Why wrong?** When one string is exhausted, you must add ALL remaining characters from the other string!

```python
# ✅ CORRECT
def scs_correct(s1, s2, n, m):
    if n == 0:
        return s2[:m]  # Add all remaining s2
    if m == 0:
        return s1[:n]  # Add all remaining s1
```

### **Mistake 2: Forgetting to Add Non-Matching Characters**

```python
# ❌ WRONG - Only adds matching characters
if s1[i-1] == s2[j-1]:
    result.append(s1[i-1])
    i -= 1
    j -= 1
# Nothing for non-matching case!
```

**Why wrong?** SCS must contain ALL characters from both strings!

```python
# ✅ CORRECT - Adds both matching and non-matching
if s1[i-1] == s2[j-1]:
    result.append(s1[i-1])  # Add once
    i -= 1
    j -= 1
elif dp[i-1][j] > dp[i][j-1]:
    result.append(s1[i-1])  # Add from s1
    i -= 1
else:
    result.append(s2[j-1])  # Add from s2
    j -= 1
```

### **Mistake 3: Wrong DP Initialization**

```python
# ❌ WRONG - Initializing with strings
dp = [['']*m for _ in range(n)]  # Wrong for LCS computation!
```

**Why wrong?** LCS DP table stores LENGTHS (integers), not strings!

```python
# ✅ CORRECT - Initialize with zeros
dp = [[0]*(m+1) for _ in range(n+1)]  # Integers for lengths
```

---

## 📊 **Complexity Analysis**

| Operation | Time | Space | Notes |
|-----------|------|-------|-------|
| **Build LCS DP** | O(n × m) | O(n × m) | Standard LCS |
| **Backtrack** | O(n + m) | O(n + m) | Linear traversal |
| **Total** | **O(n × m)** | **O(n × m)** | Dominated by DP table |

### **Space Optimization:**

You could optimize space to O(min(n, m)) for LCS computation, but then backtracking would be harder. For interview purposes, O(n × m) is standard.

---

## 🎯 **Related Problems**

### **1. Longest Common Subsequence (LCS)**
- **Relationship:** SCS uses LCS internally
- **Formula:** `SCS_length = n + m - LCS_length`

### **2. Edit Distance**
- **Similarity:** Both use DP and backtracking
- **Difference:** Edit distance counts operations, SCS builds string

### **3. Minimum Insertions/Deletions**
- **Relationship:** Related to LCS
- **Connection:** To convert s1 → s2, delete `(n - LCS)` and insert `(m - LCS)`

---

## 🧪 **Test Cases**

```python
def test_scs():
    """Comprehensive test cases"""

    test_cases = [
        # (s1, s2, expected_scs, expected_length)
        ("geek", "eke", "geeke", 5),
        ("AGGTAB", "GXTXAYB", "AGXGTXAYB", 9),

        # Edge cases
        ("abc", "def", "abcdef", 6),    # No common - just concatenate
        ("abc", "abc", "abc", 3),        # Identical - same string
        ("", "abc", "abc", 3),           # One empty
        ("abc", "", "abc", 3),           # One empty
        ("", "", "", 0),                 # Both empty

        # Single character
        ("a", "a", "a", 1),
        ("a", "b", "ab", 2),

        # Complete overlap
        ("ab", "abc", "abc", 3),
        ("abc", "ab", "abc", 3),
    ]

    for s1, s2, expected_scs, expected_len in test_cases:
        result = shortest_common_supersequence(s1, s2)
        length = scs_length_only(s1, s2)

        print(f"s1='{s1}', s2='{s2}'")
        print(f"  SCS: '{result}' (expected: '{expected_scs}')")
        print(f"  Length: {length} (expected: {expected_len})")

        # Verify
        assert len(result) == length, "Length mismatch!"
        assert is_subsequence(s1, result), f"{s1} not in SCS!"
        assert is_subsequence(s2, result), f"{s2} not in SCS!"
        print("  ✓ Passed\n")


def is_subsequence(sub: str, main: str) -> bool:
    """Check if sub is a subsequence of main"""
    i = 0
    for char in main:
        if i < len(sub) and char == sub[i]:
            i += 1
    return i == len(sub)
```

---

## 💡 **Interview Tips**

### **What to Say:**

> "The Shortest Common Supersequence problem asks for the shortest string containing both inputs as subsequences.
>
> The key insight is using the formula: `SCS_length = len(s1) + len(s2) - len(LCS)`. This works because LCS characters appear in both strings, so we count them once instead of twice.
>
> The algorithm has two steps:
> 1. Build the LCS DP table (O(n×m))
> 2. Backtrack to construct the SCS string, adding matching characters once and non-matching characters from both strings
>
> Time complexity is O(n×m) and space is O(n×m) for the DP table."

### **Common Follow-ups:**

1. **"What if we only need the length?"**
   - Just compute LCS length and use formula (no backtracking needed)

2. **"Can you optimize space?"**
   - For length only: yes, to O(min(n,m))
   - For constructing string: harder, need DP table for backtracking

3. **"What if strings are very large?"**
   - Consider space-time tradeoffs
   - Might need to reconstruct DP table during backtracking

4. **"Can there be multiple SCS?"**
   - Yes! When LCS has multiple solutions
   - Our algorithm returns one valid SCS

---

## 📚 **Key Takeaways**

1. **Formula:** `SCS_length = len(s1) + len(s2) - len(LCS)`
2. **Algorithm:** Build LCS DP, then backtrack
3. **Backtracking:** Add matching chars once, non-matching chars from both
4. **Base cases:** When one string exhausted, add all of the other
5. **Common mistake:** Forgetting to add non-matching characters

---

## 🔗 **Related Files**

- `1-longest-common-subsequence.py` - LCS implementation
- `3-print-lcs.py` - Printing LCS using backtracking
- `README.md` - Overview of all LCS problems

---

**Remember:** SCS is essentially "merging" two strings with maximum overlap (the LCS)!
