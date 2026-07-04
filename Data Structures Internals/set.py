"""
SET in Python (equivalent to C++ unordered_set)
================================================

An unordered collection of unique, hashable elements backed by a hash table.

INTERNALS
---------
- Uses open addressing with random probing (not chaining like dict pre-3.6)
- Each entry stores: hash value + element reference
- Load factor ~2/3 triggers resizing
- Resizes by powers of 2
- CPython uses a compact hash table implementation

TIME COMPLEXITY
---------------
| Operation      | Average | Worst |
|----------------|---------|-------|
| add(x)         | O(1)    | O(n)  |
| remove(x)      | O(1)    | O(n)  |
| discard(x)     | O(1)    | O(n)  |
| x in set       | O(1)    | O(n)  |
| pop()          | O(1)    | O(n)  |
| union          | O(m+n)  | O(m+n)|
| intersection   | O(min(m,n)) | O(m*n) |

Worst case occurs due to hash collisions or resizing.

SPACE COMPLEXITY: O(n)
"""

# ==============================================================================
# CREATION
# ==============================================================================

s = set()                       # empty set (NOT {} which creates empty dict)
s = {1, 2, 3}                   # set literal
s = set([1, 2, 2, 3])           # from iterable → {1, 2, 3} (duplicates removed)
s = set("hello")                # → {'h', 'e', 'l', 'o'}
s = {x for x in range(5)}       # set comprehension → {0, 1, 2, 3, 4}


# ==============================================================================
# BASIC OPERATIONS
# ==============================================================================

s = {1, 2, 3}

# Adding
s.add(4)                        # add single element → {1, 2, 3, 4}
s.update([5, 6])                # add multiple elements → {1, 2, 3, 4, 5, 6}

# Removing
s.remove(6)                     # remove element (KeyError if not found)
s.discard(100)                  # remove element (NO error if not found) - SAFER
s.pop()                         # remove and return arbitrary element
s.clear()                       # remove all elements


# ==============================================================================
# MEMBERSHIP TEST - O(1)
# ==============================================================================

s = {1, 2, 3, 4, 5}

print(3 in s)                   # True  - O(1) lookup
print(10 in s)                  # False - O(1) lookup
print(10 not in s)              # True


# ==============================================================================
# SET OPERATIONS
# ==============================================================================

a = {1, 2, 3}
b = {2, 3, 4}

# Union - elements in either set
a | b                           # → {1, 2, 3, 4}
a.union(b)                      # same as above

# Intersection - elements in both sets
a & b                           # → {2, 3}
a.intersection(b)               # same as above

# Difference - elements in a but not in b
a - b                           # → {1}
a.difference(b)                 # same as above

# Symmetric Difference - elements in either but not both
a ^ b                           # → {1, 4}
a.symmetric_difference(b)       # same as above


# ==============================================================================
# IN-PLACE SET OPERATIONS (modify original set)
# ==============================================================================

a = {1, 2, 3}
b = {2, 3, 4}

a |= b                          # a.update(b) - union
a &= b                          # a.intersection_update(b)
a -= b                          # a.difference_update(b)
a ^= b                          # a.symmetric_difference_update(b)


# ==============================================================================
# SUBSET / SUPERSET CHECKS
# ==============================================================================

a = {1, 2}
b = {1, 2, 3, 4}

a <= b                          # True - a is subset of b
a.issubset(b)                   # same as above

b >= a                          # True - b is superset of a
b.issuperset(a)                 # same as above

a < b                           # True - proper subset (subset but not equal)
b > a                           # True - proper superset

a.isdisjoint({5, 6})            # True - no common elements


# ==============================================================================
# HASHABILITY REQUIREMENT
# ==============================================================================

# Elements MUST be hashable (immutable)

valid_set = {1, "hello", (1, 2), frozenset([3, 4])}  # all hashable

# invalid_set = {[1, 2]}        # TypeError: unhashable type: 'list'
# invalid_set = {{1, 2}}        # TypeError: unhashable type: 'set'
# invalid_set = {{"a": 1}}      # TypeError: unhashable type: 'dict'


# ==============================================================================
# FROZENSET - IMMUTABLE SET
# ==============================================================================

fs = frozenset([1, 2, 3])       # immutable version of set

# Can be used as:
# - Dictionary key
# - Element of another set

d = {frozenset([1, 2]): "value"}  # valid
nested = {frozenset([1, 2]), frozenset([3, 4])}  # set of sets


# ==============================================================================
# COMMON USE CASES
# ==============================================================================

# 1. Remove duplicates from list (order not preserved)
nums = [1, 2, 2, 3, 3, 3]
unique = list(set(nums))        # [1, 2, 3] (order may vary)

# 2. Remove duplicates preserving order (Python 3.7+)
unique_ordered = list(dict.fromkeys(nums))  # [1, 2, 2, 3]

# 3. Fast membership testing
valid_ids = {101, 102, 103, 104, 105}
if user_id in valid_ids:        # O(1) instead of O(n) for list
    pass

# 4. Find common elements
list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
common = set(list1) & set(list2)  # {3, 4}

# 5. Find unique elements
only_in_list1 = set(list1) - set(list2)  # {1, 2}

# 6. Check for duplicates
def has_duplicates(lst):
    return len(lst) != len(set(lst))


# ==============================================================================
# SET vs LIST for LOOKUP
# ==============================================================================

# List lookup: O(n)
# Set lookup: O(1)

# Use set when:
# - Need fast membership testing
# - Don't need ordering
# - Don't need duplicates
# - Elements are hashable

# Use list when:
# - Need ordering
# - Need duplicates
# - Need indexing
# - Elements may be unhashable
