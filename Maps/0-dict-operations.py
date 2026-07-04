# Dictionary/Map Operations & defaultdict

from collections import defaultdict

# ============================================
# 1. GET KEYS, VALUES, ITEMS
# ============================================

d = {'a': 1, 'b': 2, 'c': 3}

keys = d.keys()              # dict_keys(['a', 'b', 'c'])
values = d.values()          # dict_values([1, 2, 3])
items = d.items()            # dict_items([('a', 1), ('b', 2), ('c', 3)])

# Convert to list
keys_list = list(d.keys())   # ['a', 'b', 'c']
values_list = list(d.values())  # [1, 2, 3]

# Iterate
for key in d.keys():
    print(key)
for key, value in d.items():
    print(f"{key}: {value}")


# ============================================
# 2. DEFAULTDICT - Auto initialize missing keys
# ============================================

# Without defaultdict - KeyError risk
d = {}
# d['a'] += 1  # KeyError: 'a'

# With defaultdict(int) - auto-initializes to 0
count = defaultdict(int)
count['a'] += 1
count['b'] += 2
print(count)  # defaultdict(<class 'int'>, {'a': 1, 'b': 2})

# defaultdict(list) - auto-initializes to []
groups = defaultdict(list)
groups['a'].append(1)
groups['a'].append(2)
groups['b'].append(3)
print(groups)  # defaultdict(<class 'list'>, {'a': [1, 2], 'b': [3]})

# defaultdict(set) - auto-initializes to set()
unique = defaultdict(set)
unique['a'].add(1)
unique['a'].add(2)
unique['a'].add(1)  # Duplicate ignored
print(unique)  # defaultdict(<class 'set'>, {'a': {1, 2}})


# ============================================
# 3. DEFAULTDICT WITH LAMBDA (Custom default)
# ============================================

dd = defaultdict(lambda: 0)
dd['x'] += 5
print(dd)  # defaultdict(<function ...>, {'x': 5})

dd_list = defaultdict(lambda: [])
dd_list['fruits'].append('apple')
dd_list['fruits'].append('banana')
print(dd_list)  # defaultdict(<function ...>, {'fruits': ['apple', 'banana']})

dd_nested = defaultdict(lambda: defaultdict(int))
dd_nested['user1']['count'] += 1
dd_nested['user1']['score'] += 10
print(dd_nested)  # Nested defaultdict


# ============================================
# 4. MULTIPLE OPERATIONS - Common Patterns
# ============================================

# Pattern 1: Count frequency
text = "hello"
freq = defaultdict(int)
for char in text:
    freq[char] += 1
print(freq)  # defaultdict(<class 'int'>, {'h': 1, 'e': 1, 'l': 2, 'o': 1})

# Pattern 2: Group by value
nums = [1, 2, 3, 4, 5, 6]
by_parity = defaultdict(list)
for num in nums:
    by_parity[num % 2].append(num)  # Group by odd/even
print(by_parity)  # {0: [2, 4, 6], 1: [1, 3, 5]}

# Pattern 3: Build adjacency list (Graph)
edges = [(1, 2), (1, 3), (2, 3)]
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)  # For undirected
print(graph)  # {1: [2, 3], 2: [1, 3], 3: [1, 2]}

# Pattern 4: Anagram grouping
words = ["eat", "tea", "ate", "bat", "tab"]
anagrams = defaultdict(list)
for word in words:
    key = ''.join(sorted(word))  # Sort chars to get canonical form
    anagrams[key].append(word)
print(anagrams)  # {'aet': ['eat', 'tea', 'ate'], 'abt': ['bat', 'tab']}


# ============================================
# 5. DICT COMPREHENSION
# ============================================

# Simple dict comprehension
squares = {x: x**2 for x in range(5)}
print(squares)  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# With condition
evens = {x: x**2 for x in range(10) if x % 2 == 0}
print(evens)  # {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# From list of tuples
pairs = [('a', 1), ('b', 2), ('c', 3)]
d = {k: v for k, v in pairs}
print(d)  # {'a': 1, 'b': 2, 'c': 3}

# Invert keys and values
d = {'a': 1, 'b': 2, 'c': 3}
inverted = {v: k for k, v in d.items()}
print(inverted)  # {1: 'a', 2: 'b', 3: 'c'}

# Defaultdict comprehension (still need to use defaultdict constructor)
dd = defaultdict(int, {x: 0 for x in range(5)})
print(dd)  # defaultdict with pre-populated keys


# ============================================
# 6. COMMON METHODS
# ============================================

d = {'a': 1, 'b': 2}

d.get('a')              # Returns 1
d.get('z')              # Returns None
d.get('z', 0)           # Returns 0 (default value)

d.pop('a')              # Removes 'a', returns 1
d.pop('z', None)        # Returns None if not found

d.setdefault('c', 3)    # Sets 'c': 3 if not exists, returns value

d.update({'x': 10})     # Add/update multiple items

d.clear()               # Remove all items

d.copy()                # Shallow copy
