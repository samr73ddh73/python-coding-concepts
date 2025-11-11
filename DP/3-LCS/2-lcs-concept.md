## 🔤 Longest Common Substring vs Subsequence

### Key Difference:

| Problem | Continuity | When No Match | Answer Location |
|---------|------------|---------------|-----------------|
| **Subsequence** | Can skip chars | `max(dp[i-1][j], dp[i][j-1])` | `dp[n][m]` ✅ |
| **Substring** | Must be continuous | `dp[i][j] = 0` (reset!) | `max(all dp[i][j])` ⚠️ |

### Longest Common Substring:

**Problem:** Find longest **continuous** common substring (not subsequence!)

**Example:**
```python
s1 = "abcde"
s2 = "xabcdy"
# Longest common substring: "abcd" (length 4)
# Must be continuous!
```

**Key Insight:** `dp[i][j]` = length of substring **ending at** `s1[i-1]` and `s2[j-1]`

**Algorithm:**
```python
if s1[i-1] == s2[j-1]:
    dp[i][j] = dp[i-1][j-1] + 1  # Extend substring
    max_length = max(max_length, dp[i][j])  # Track global max
else:
    dp[i][j] = 0  # Substring breaks (not continuous)
```

**Why need global max?**
- When chars don't match, `dp[i][j] = 0` (substring ends)
- The longest substring might have **already ended** before reaching `(n, m)`
- Unlike subsequence, answer does **NOT propagate** to `dp[n][m]`
- Must track maximum across **all positions**

**Example showing why:**
```
s1 = "abc", s2 = "xaby"

DP Table:
       ""  x  a  b  y
""      0  0  0  0  0
a       0  0  1  0  0  ← "a" (length 1)
b       0  0  0  2  0  ← "ab" (length 2) ✓ MAX HERE!
c       0  0  0  0  0  ← chars don't match, resets to 0

dp[3][4] = 0 (last position)
But answer = 2 (at dp[2][3])
```

**Bottom-up approach:**
```python
def longest_common_substring(s1, s2):
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    max_length = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                max_length = max(max_length, dp[i][j])
            # else: dp[i][j] = 0 (already initialized)

    return max_length
```

**Time:** O(n × m)
**Space:** O(n × m) - can optimize to O(min(n, m))

**Remember:**
- Subsequence: Answer at `dp[n][m]` (propagates via `max()`)
- Substring: Answer anywhere in table (need global max tracking)