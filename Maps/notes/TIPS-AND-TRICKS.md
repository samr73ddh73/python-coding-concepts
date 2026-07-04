# 🎯 Maps/Dictionaries Tips & Tricks

> Essential tips for dictionary and hash map problems

---

## Core Tips

### defaultdict - Auto-Initialization

**Game Changer:** No need to check if key exists!

```python
from collections import defaultdict

# Bad: Manual checking
if key not in d:
    d[key] = []
d[key].append(value)

# Good: defaultdict
d = defaultdict(list)
d[key].append(value)  # Auto-creates [] if missing
```

**Common Initializers:**
```python
defaultdict(int)    # Default: 0
defaultdict(list)   # Default: []
defaultdict(set)    # Default: set()
defaultdict(str)    # Default: ""
```

### Counter - Frequency Counting

```python
from collections import Counter

# Count elements
freq = Counter(nums)
freq['a'] += 1

# Get most common
freq.most_common(k)  # Top k elements with counts

# Compare frequencies
Counter(s1) == Counter(s2)  # Are they anagrams?
```

### Dictionary Operations

| Operation | Time | Notes |
|---|---|---|
| Access `d[key]` | O(1) | Raises KeyError if missing |
| Check `key in d` | O(1) | Membership check |
| `d.get(key, default)` | O(1) | Returns default if missing |
| `d.pop(key)` | O(1) | Remove and return |
| `d.update(other)` | O(n) | Merge dictionaries |

---

## Common Patterns

### Pattern 1: Group Elements

```python
# Group numbers by their value
groups = defaultdict(list)
for num in nums:
    groups[num].append(num)

# Group strings by sorted chars (anagrams)
anagrams = defaultdict(list)
for word in words:
    key = ''.join(sorted(word))
    anagrams[key].append(word)
```

### Pattern 2: Two-Sum with Hash Map

```python
seen = {}
for num in nums:
    complement = target - num
    if complement in seen:
        return [seen[complement], i]
    seen[num] = i
return []
```

### Pattern 3: Invert Keys and Values

```python
d = {'a': 1, 'b': 2, 'c': 3}
inverted = {v: k for k, v in d.items()}
# {1: 'a', 2: 'b', 3: 'c'}
```

---

## Key Insights

**Use dict, not list, for O(1) lookup:**
```python
# Bad: O(n) membership check
if num in [1, 2, 3, 4, 5]:
    pass

# Good: O(1) membership check
if num in {1, 2, 3, 4, 5}:
    pass
```

**defaultdict saves code:**
```python
# No need to handle KeyError
d = defaultdict(int)
d[key] += 1  # Works even if key doesn't exist
```

**Counter is cleaner for frequency:**
```python
# Count characters
from collections import Counter
freq = Counter("aabbc")
# Counter({'a': 2, 'b': 2, 'c': 1})
```

---

## Time & Space Complexity

| Problem | Time | Space |
|---|---|---|
| Two Sum | O(n) | O(n) |
| Group anagrams | O(n·k log k) | O(n) |
| Frequency count | O(n) | O(k) |
| Intersection | O(min(m,n)) | O(min(m,n)) |
| Union | O(m+n) | O(m+n) |

---

## Edge Cases

- Empty dictionary
- All same keys (overwrite)
- All unique keys
- Nested dictionaries
- Dictionary as value/key considerations

---

## Interview Tips

1. **Always use dict for O(1) lookup, not list**
2. **defaultdict for auto-initialization** 
3. **Counter for frequency problems**
4. **Be careful with mutable keys** (lists can't be keys, tuples can)
5. **Mention space-time tradeoff** (O(n) space for O(1) lookup)

---

*Tips for hash map and dictionary problems*
