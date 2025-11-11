# Longest Common Subsequence (LCS) Problems

This folder contains variations of the Longest Common Subsequence problem.

---

## 📚 Problem Types

### 1. Longest Common Subsequence (LCS)
**File:** `1-longest-common-subsequence.py`

**Problem:** Find the length of the longest subsequence common to both strings.

**Key:** Characters can be **skipped** (non-continuous)

**Example:**
```
s1 = "abcde"
s2 = "ace"
LCS = "ace" (length 3)
```

**DP Definition:** `dp[i][j]` = max length using `s1[0..i-1]` and `s2[0..j-1]`

**Recurrence:**
```python
if s1[i-1] == s2[j-1]:
    dp[i][j] = 1 + dp[i-1][j-1]
else:
    dp[i][j] = max(dp[i-1][j], dp[i][j-1])  # Try skipping from either string
```

**Answer:** `dp[n][m]` ✅ (propagates to final position)

---

### 2. Longest Common Substring ⚠️
**File:** `2-longest-common-substring.py`

**Problem:** Find the length of the longest **continuous** common substring.

**Key:** Characters must be **consecutive** (continuous)

**Example:**
```
s1 = "abcde"
s2 = "xabcdy"
Longest common substring = "abcd" (length 4)
# Must be continuous!
```

**DP Definition:** `dp[i][j]` = length of substring **ending at** `s1[i-1]` and `s2[j-1]`

**Recurrence:**
```python
if s1[i-1] == s2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1      # Extend substring
    max_length = max(max_length, dp[i][j])  # Track max!
else:
    dp[i][j] = 0  # Substring breaks (reset!)
```

**Answer:** `max(all dp[i][j])` ⚠️ (need to track global maximum)

**Why different from subsequence?**
- Substring resets to 0 when chars don't match
- Answer might be anywhere in the table, not just at `dp[n][m]`
- Must track maximum seen across all positions

---

## 🔑 Key Differences

| Aspect | Subsequence | Substring |
|--------|-------------|-----------|
| **Continuity** | Can skip characters | Must be consecutive |
| **When no match** | `max(dp[i-1][j], dp[i][j-1])` | `dp[i][j] = 0` |
| **Answer location** | `dp[n][m]` | `max(all dp[i][j])` |
| **Example** | "abc" in "aXbXc" ✅ | "abc" in "aXbXc" ❌ |

### Visual Example:

**Input:** `s1 = "abc"`, `s2 = "xaby"`

#### Subsequence DP Table:
```
       ""  x  a  b  y
""      0  0  0  0  0
a       0  0  1  1  1  ← carries forward →
b       0  0  1  2  2  ← carries forward →
c       0  0  1  2  2  ← carries forward →
                    ^
              Answer at dp[3][4] = 2 ✅
```

#### Substring DP Table:
```
       ""  x  a  b  y
""      0  0  0  0  0
a       0  0  1  0  0  ← "a" (length 1)
b       0  0  0  2  0  ← "ab" (length 2) ✓ MAX!
c       0  0  0  0  0  ← resets to 0
                    ^
              dp[3][4] = 0
              But max seen = 2 ✅
```

---

## 🎯 Interview Tips

### For Subsequence:
- Answer always at `dp[n][m]`
- Can skip characters
- More common in interviews

### For Substring:
- **Must track global maximum!** ⚠️
- Cannot skip characters
- Often confused with subsequence
- Remember: "substring = continuous"

### Common Follow-ups:
1. Print the actual LCS/substring (not just length)
2. Find all LCS (multiple solutions)
3. Space optimization to O(min(m,n))
4. What if strings are very large?

---

## 📊 Complexity

| Approach | Time | Space |
|----------|------|-------|
| Top-down memo | O(m × n) | O(m × n) + O(m+n) stack |
| Bottom-up 2D | O(m × n) | O(m × n) |
| Space-optimized | O(m × n) | O(min(m, n)) |

---

## 🧪 Test Cases to Remember

```python
# Edge cases
s1 = "", s2 = "abc"  → 0
s1 = "abc", s2 = ""  → 0
s1 = "abc", s2 = "abc"  → 3 (both problems)
s1 = "abc", s2 = "def"  → 0 (no common)

# Different results
s1 = "abcde", s2 = "ace"
# Subsequence: 3 ("ace")
# Substring: 1 ("a" or "c" or "e")
```

---

## 🔗 Related Problems

- Edit Distance
- Shortest Common Supersequence
- Longest Palindromic Subsequence
- Minimum Insertions/Deletions to convert s1 to s2

---

**Remember:** Substring needs **global max tracking** because answer doesn't propagate to `dp[n][m]`!
