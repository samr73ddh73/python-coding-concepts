# Word Ladder Pattern

## Problem: Word Ladder
**LeetCode 127** | [Problem Link](https://leetcode.com/problems/word-ladder/description/)

Given two words, `beginWord` and `endWord`, and a dictionary `wordList`, return the number of words in the shortest transformation sequence from `beginWord` to `endWord`, or `0` if no such sequence exists.

A transformation sequence is valid if:
- Each word differs from the previous by exactly **one letter**
- Each intermediate word must exist in `wordList`

**Example**:
```
beginWord = "hit"
endWord = "cog"
wordList = ["hot","dot","dog","lot","log","cog"]

Output: 5
Explanation: "hit" → "hot" → "dot" → "dog" → "cog"
```

---

## Why This is a Graph Problem

### Recognition Triggers

```
Q1: Do I have entities with relationships?
    ↓
    Yes: Words that differ by 1 letter

Q2: Do I need to find a path between two entities?
    ↓
    Yes: Path from beginWord to endWord

Q3: Is it the shortest path?
    ↓
    Yes: "transformation sequence"

→ Answer: GRAPH + BFS (shortest path in unweighted graph)
```

### Graph Representation

```
Nodes = Words in wordList + beginWord
Edges = Connect words that differ by exactly 1 letter

Example:
"hit" ↔ "hot" (differ in position 0)
"hot" ↔ "dot" (differ in position 0)
"hot" ↔ "lot" (differ in position 0)
"dot" ↔ "dog" (differ in position 2)
"lot" ↔ "log" (differ in position 2)
"dog" ↔ "cog" (differ in position 0)
"log" ↔ "cog" (differ in position 2)

Visual:
      hit
       ↓
      hot
     / | \
   dot | lot
   |   |   |
  dog  × log
    \  |  /
      cog
```

**Graph Type**: Unweighted, undirected → **BFS finds shortest path**

---

## Initial Solution (Your Approach)

```python
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        def isTransformationPossible(s1, s2):
            ct = 0
            for i in range(len(s1)):
                if s1[i] != s2[i]:
                    if ct >= 1:
                        return False
                    else:
                        ct += 1
            return True

        if endWord not in wordList:
            return 0
        
        queue = deque([(beginWord, 1)])
        visited = set()
        visited.add(beginWord)
        
        while queue:
            word, dist = queue.popleft()
            
            if word == endWord:
                return dist
            
            for w in wordList:  # ❌ Check ALL words
                t = isTransformationPossible(word, w)  # ❌ For each word
                if w not in visited and t:
                    queue.append((w, dist + 1))
                    visited.add(w)
        
        return 0
```

**Time Complexity**: **O(n² · m)**
- `n` = length of wordList
- `m` = length of word

**Why**: For every word processed in BFS, check **all** words in wordList, each comparison takes O(m)

---

## Problems with Initial Approach

### ❌ Problem 1: Inefficient Neighbor Finding
```python
for w in wordList:  # O(n)
    t = isTransformationPossible(word, w)  # O(m)
    # Total: O(n · m) per word
```

You check **every word** to see if it's a neighbor. This is slow.

### ❌ Problem 2: Redundant Comparisons
```
Processing "hit":
  - Compare with "hot" ✓ (neighbor)
  - Compare with "dot" ✗
  - Compare with "dog" ✗
  - Compare with "lot" ✗
  - Compare with "log" ✗
  - Compare with "cog" ✗
  (5 wasted comparisons)

Processing "hot":
  - Compare with "hit" (already visited)
  - Compare with "dot" ✓ (neighbor)
  - Compare with "dog" ✗
  - ...
  (more wasted comparisons)
```

### Example of Slowness
```
wordList = ["hit", "hot", "dot", "dog", "lot", "log", "cog"]
n = 7, m = 3

For each word:
  Check all 7 words
  Each comparison: 3 operations
  
Total: 7 * 7 * 3 = 147 operations

With optimization: ~50 operations (see below)
```

---

## Optimal Solution

### Key Insight: Generate Neighbors Instead of Checking All Words

```python
# Instead of:
for w in wordList:
    if isTransformationPossible(word, w):
        ...

# Do this:
for i in range(len(word)):
    for c in 'abcdefghijklmnopqrstuvwxyz':
        neighbor = word[:i] + c + word[i+1:]
        if neighbor in wordSet:
            ...
```

**Why**: Only check ~26m possible neighbors, not all n words

### Complete Optimal Solution

```python
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        if endWord not in wordList:
            return 0
        
        # Convert to set for O(1) lookup
        wordSet = set(wordList)
        queue = deque([(beginWord, 1)])
        visited = {beginWord}
        
        while queue:
            word, dist = queue.popleft()
            
            if word == endWord:
                return dist
            
            # Generate all possible neighbors (one letter change)
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    neighbor = word[:i] + c + word[i+1:]
                    
                    # Check if neighbor exists in wordList
                    if neighbor in wordSet and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, dist + 1))
        
        return 0
```

**Time Complexity**: **O(n · m · 26)** = **O(n · m)**
- `n` = number of words (max words we process)
- `m` = word length
- `26` = alphabet size (constant)

---

## Complexity Comparison

| Approach | Time | Space | Why |
|----------|------|-------|-----|
| **Initial (Check all words)** | O(n² · m) | O(n) | For each word, check all n words |
| **Optimal (Generate neighbors)** | O(n · m · 26) | O(n) | For each word, generate 26m neighbors |

**Speed Improvement**: ~10-100x faster for typical inputs

---

## Step-by-Step Example

```
beginWord = "hit"
endWord = "cog"  
wordSet = {"hot", "dot", "dog", "lot", "log", "cog"}

Step 1: word="hit", dist=1
  i=0: Generate "ait", "bit", ..., "hot" (found!)
       Add "hot" to queue
  i=1: Generate "hat", "hbt", ...
  i=2: Generate "hia", "hib", ...

Step 2: word="hot", dist=2
  i=0: Generate "aot", "bot", ..., "dot" (found!)
       Add "dot" to queue
  i=1: Generate "hat" (visited), "hbt", ...
  i=2: Generate "hoa", "hob", ...

Step 3: word="dot", dist=3
  i=0: Generate "aot" (visited), ..., "hot" (visited), ...
  i=1: Generate "dat", "dbt", ...
  i=2: Generate "doa", "dob", ..., "dog" (found!)
       Add "dog" to queue

Step 4: word="lot", dist=3
  i=0: Generate "aot" (visited), ..., "log" (found!)
       Add "log" to queue
  ...

Step 5: word="dog", dist=4
  i=0: Generate "aog", "bog", ..., "cog" (found!)
       Add "cog" to queue
  ...

Step 6: word="cog", dist=5
  word == endWord → return 5
```

---

## Key Differences

### Generating Neighbors (Optimal)
```python
for i in range(len(word)):  # 3 iterations
    for c in 'abc...xyz':   # 26 iterations
        # Total: 3 * 26 = 78 checks
        # But only valid ones are neighbors
```

### Checking All Words (Initial)
```python
for w in wordList:  # 7 iterations
    # Check each word: 7 comparisons
    # But only 1-2 are actual neighbors
```

---

## When to Use This Pattern

| Pattern | Use Case | Example |
|---------|----------|---------|
| **Generate neighbors** | Small alphabet (26 letters) | Word Ladder, DNA mutations |
| **Check all candidates** | Large, sparse graph | Social network connections |

For Word Ladder: **Always generate neighbors** (alphabet is fixed at 26)

---

## Common Mistakes

1. ❌ Checking all words in wordList for every word
   - ✅ Generate possible neighbors (26m variants)

2. ❌ Using list for wordList lookups
   - ✅ Convert to set for O(1) lookups

3. ❌ Not checking if endWord exists before BFS
   - ✅ Return 0 immediately if endWord not in wordList

4. ❌ Forgetting to mark visited before enqueueing
   - ✅ Add to visited immediately to avoid duplicates

---

## Similar Problems

1. **LeetCode 752** (Open the Lock) — BFS with state generation
   - Generate 8 neighbor states (4 positions × 2 directions)

2. **LeetCode 909** (Snakes and Ladders) — BFS on grid
   - Similar shortest path, but on a board

3. **LeetCode 433** (Minimum Genetic Mutation) — Similar to Word Ladder
   - Same pattern: find shortest sequence of 1-character changes

4. **LeetCode 1306** (Jump Game III) — Graph traversal
   - BFS/DFS to find reachability

---

## Template: Generate Neighbors Pattern

```python
def shortestPath(start, end, candidates):
    if end not in candidates:
        return 0
    
    # Convert to set for O(1) lookup
    candidateSet = set(candidates)
    queue = deque([(start, 1)])
    visited = {start}
    
    while queue:
        current, dist = queue.popleft()
        
        if current == end:
            return dist
        
        # Generate all possible neighbors
        for neighbor in generateNeighbors(current):
            if neighbor in candidateSet and neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    
    return 0

def generateNeighbors(word):
    """Generate all 1-step transformations"""
    neighbors = []
    for i in range(len(word)):
        for c in 'abcdefghijklmnopqrstuvwxyz':
            if c != word[i]:
                neighbor = word[:i] + c + word[i+1:]
                neighbors.append(neighbor)
    return neighbors
```

---

## Key Takeaway

**For problems with small, fixed alphabets, generate candidates instead of checking all existing items. This turns O(n · m) into O(m) per step.**

When you see "one step at a time," think "generate neighbors, not check all."
