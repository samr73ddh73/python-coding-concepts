# DSU (Disjoint Set Union) / Union-Find — Quick Notes

## What is DSU?

A **data structure** to manage groups of elements where:
- Elements can be added to groups
- You can quickly check if two elements are in the same group
- You can merge two groups

Think of it as: **"Which group does element X belong to? Are X and Y in the same group?"**

---

## When to Use DSU?

```
Problem involves:
├─ "Are two nodes connected?" → DSU ✓
├─ "Do they belong to same group?" → DSU ✓
├─ "Connect two groups" → DSU ✓
├─ "Detect cycles in graph" → DSU ✓
├─ "Find connected components" → DSU ✓
└─ "Network connectivity" → DSU ✓
```

**Common Problems:**
- Cycle detection in undirected graph
- Connected components
- Redundant connections
- Friend circles
- Network connectivity
- Kruskal's algorithm (MST)

---

## The Algorithm: Two Core Operations

### 1. FIND(x) — What group does x belong to?

**Naive approach:**
```
Find parent of x, then parent of parent, ... until you reach root
```

**Example:**
```
        1 (root)
       / \
      2   3
     /
    4

Find(4):
  4's parent is 2
  2's parent is 1
  1's parent is 1 (root)
  → Return 1 (they belong to group 1)
```

**Code:**
```python
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])  # Path compression (optimization)
    return parent[x]
```

### 2. UNION(x, y) — Merge group of x with group of y

**Steps:**
1. Find root of x (root_x)
2. Find root of y (root_y)
3. Connect root_x to root_y (make one parent of other)

**Example:**
```
Group 1:      Group 2:
    1             5
   / \           /
  2   3         6

Union(2, 6):
  Find(2) = 1
  Find(6) = 5
  Connect: parent[1] = 5
  
Result:
      5
     / \
    1   6
   / \
  2   3
```

**Code:**
```python
def union(x, y):
    root_x = find(x)
    root_y = find(y)
    
    if root_x != root_y:
        parent[root_x] = root_y  # Make root_y parent of root_x
```

---

## Simple Implementation

```python
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))  # Initially, each element is its own parent
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same group
        
        # Union by rank - attach smaller tree to larger
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        return True  # Successfully merged
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

---

## Visual Example: Cycle Detection

**Problem:** Detect if undirected graph has a cycle

**Graph:**
```
Edges: (1,2), (2,3), (3,4), (4,1)

    1 --- 2
    |     |
    4 --- 3
```

**Step-by-step:**
```
Initial: 1→1, 2→2, 3→3, 4→4 (each is own group)

Edge (1,2):
  find(1)=1, find(2)=2 (different groups)
  → union(1,2): 1→2
  Groups: 1,2 together | 3 | 4

Edge (2,3):
  find(2)=2, find(3)=3 (different groups)
  → union(2,3): 2→3
  Groups: 1,2,3 together | 4
  
Edge (3,4):
  find(3)=3, find(4)=4 (different groups)
  → union(3,4): 3→4
  Groups: 1,2,3,4 all together

Edge (4,1):
  find(4)=4, find(1)=? 
  → find(1): 1→2, 2→3, 3→4, 4→4 = 4
  → find(1)=4, find(4)=4 (SAME GROUP!)
  → CYCLE DETECTED! ✓
```

---

## Optimizations Explained

### 1. PATH COMPRESSION

**Without optimization:**
```
Deep chain:
1 → 2 → 3 → 4 → 5 (root)
find(1) takes 4 steps to reach 5
```

**With Path Compression:**
```
After find(1), restructure to:
  1
  2    3    4
    ↓   ↓   ↓
      5 (root)

find(1) next time = 1 step! ✓
```

**Code:**
```python
def find(x):
    if self.parent[x] != x:
        self.parent[x] = self.find(self.parent[x])  # This line does it
    return self.parent[x]
```

### 2. UNION BY RANK

**Without optimization:**
```
Union by just picking random parent:
  1          2
  |        /|\
  3      4 5 6
  |
  4    → After union, very unbalanced tree!
```

**With Union by Rank:**
```
Attach smaller tree to larger:
  2          1
/|\          |
4 5 6        3
             |
             2
          /|\
         4 5 6    → More balanced!
```

**Intuition:** Keep tree shallow so find() is fast

---

## Time Complexity

### Without Optimizations
- Find: O(n) worst case (linear chain)
- Union: O(n) (calls find)

### With Path Compression Only
- Find: O(log n) amortized
- Union: O(log n) amortized

### With Path Compression + Union by Rank
- Find: O(α(n)) — almost O(1)!
- Union: O(α(n))

**Where α(n) = Inverse Ackermann function**
```
α(n) is practically constant for all reasonable n
α(5) = 3, α(10^80) = 4

So effectively: O(1) per operation!
```

---

## Example: Redundant Connection Problem

**Problem:** Given edges, find the edge that creates a cycle

```python
def findRedundantConnection(edges):
    dsu = DSU(len(edges) + 1)
    
    for u, v in edges:
        if dsu.connected(u, v):
            # u and v already in same component → this edge creates cycle!
            return [u, v]
        dsu.union(u, v)
    
    return []
```

**Example:**
```
Edges: [[1,2], [1,3], [2,3]]

Process [1,2]: connect 1-2
Process [1,3]: connect 1-3
Process [2,3]: 
  find(2)=2, find(3)=3 ... wait actually:
  find(2)→1, find(3)→1 (both in component 1)
  → Already connected! Return [2,3]
```

---

## Quick Checklist Before Using DSU

✓ Checking if two nodes are connected?
✓ Need to efficiently merge groups?
✓ Problem mentions "cycles", "components", "connectivity"?
✓ Graph is undirected?
✓ Need fast repeated unions/finds?

→ **USE DSU!**

---

## Space Complexity

- **Space:** O(n) for parent array and rank array
- That's it! Very memory efficient compared to other approaches
