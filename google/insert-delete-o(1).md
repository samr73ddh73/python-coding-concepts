https://leetcode.com/problems/insert-delete-getrandom-o1/description/

Here are concise notes for this problem:

## Problem: Insert Delete GetRandom O(1) - Duplicates Allowed

Design a data structure supporting O(1) insert, remove, and getRandom with duplicates.
- `insert(val)`: Add val (even if exists), return true if first occurrence
- `remove(val)`: Remove one occurrence, return true if existed
- `getRandom()`: Return random element with probability proportional to frequency

---

## Key Concepts

### Why Array for Random?
**Only arrays provide O(1) random access by index**

```python
# Array: O(1) ✓
random_element = array[random_index]

# Set: O(n) ✗ - must convert to list first
random_element = random.choice(list(my_set))
```

Arrays store elements in contiguous memory → direct index calculation:
`address = base + (index × size)` = O(1)

### Why Not Just Set/HashMap?
- **Set/HashMap**: No indexing, can't do `my_set[2]`
- **Array alone**: Remove from middle is O(n) (must shift elements)
- **Solution**: Combine both!

### O(1) Remove Trick: Swap with Last
```python
# Instead of shifting elements:
array = [10, 20, 30, 40]
         ↑           ↑
      remove      last

# Swap with last, then pop
array = [10, 40, 30, 40]
array.pop()  # O(1)
array = [10, 40, 30]
```

### Data Structures
- `array`: Store all elements (with duplicates) → O(1) random access
- `indexDict`: Map value → set of indices → O(1) lookup for remove

---

## Solution

```python
from collections import defaultdict
from random import choice

class RandomizedCollection:
    def __init__(self):
        self.array = []
        self.indexDict = defaultdict(set)

    def insert(self, val: int) -> bool:
        self.array.append(val)
        if val in self.indexDict:
            self.indexDict[val].add(len(self.array)-1)
            return False
        self.indexDict[val].add(len(self.array)-1)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.indexDict:
            return False
        
        # Get any index of val to remove
        indx = self.indexDict[val].pop()
        if len(self.indexDict[val]) == 0:
            del self.indexDict[val]
        
        # If removing last element, just pop
        if indx == len(self.array)-1:
            self.array.pop()
        else:
            # Swap with last element
            last = self.array[-1]
            self.array[indx] = last
            self.indexDict[last].remove(len(self.array)-1)
            self.array.pop()
            self.indexDict[last].add(indx)
        
        return True

    def getRandom(self) -> int:
        return choice(self.array)
```

**Time Complexity**: O(1) average for all operations  
**Space Complexity**: O(n)

---

## Quick Reference

| Structure | Purpose | Why |
|-----------|---------|-----|
| Array | getRandom() | Only O(1) indexing |
| HashMap | insert/remove | O(1) lookup of indices |
| Set (in dict) | Track duplicates | Multiple indices per value |

**Key insight**: Duplicates in array → weighted probability automatically! 🎲