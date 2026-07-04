# 🎯 Backtracking Tips & Tricks

> Essential patterns and insights for backtracking problems

---

## Core Concept

**Backtracking = Recursion + Pruning**

Explore all possibilities but **prune** branches that can't lead to solution.

```python
def backtrack(path, candidates):
    if is_valid_solution(path):
        results.append(path[:])  # Found solution
        return
    
    for choice in candidates:
        if is_valid_choice(choice):
            path.append(choice)
            backtrack(path, remaining_candidates)
            path.pop()  # Backtrack: undo choice
```

---

## Key Patterns

### Pattern 1: Permutations

```python
def permute(nums):
    result = []
    def backtrack(path, remaining):
        if not remaining:
            result.append(path)
            return
        for i, num in enumerate(remaining):
            backtrack(path + [num], remaining[:i] + remaining[i+1:])
    backtrack([], nums)
    return result
```

**Key:** Use all elements exactly once

### Pattern 2: Combinations

```python
def combine(n, k):
    result = []
    def backtrack(start, path):
        if len(path) == k:
            result.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1, path)  # Start from i+1 to avoid duplicates
            path.pop()
    backtrack(1, [])
    return result
```

**Key:** Choose k elements, order doesn't matter, no repeats

### Pattern 3: Subsets

```python
def subsets(nums):
    result = []
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    backtrack(0, [])
    return result
```

**Key:** All possible subsets (including empty and full)

---

## Critical Tips

### 1. Pass by Reference vs Value

**IMP: Use `path[:]` to copy, not just `path`!**

```python
# Bad: All results point to same list!
result.append(path)

# Good: Copy the list
result.append(path[:])
# Or
result.append(list(path))
```

### 2. Backtrack/Undo Changes

```python
path.append(choice)      # Make choice
backtrack(...)           # Explore
path.pop()               # Undo choice (CRITICAL!)
```

**Don't forget the `pop()`!** Otherwise state pollution.

### 3. Pruning - Cut Branches Early

```python
# Pruning example: subset sum
def backtrack(start, path, target):
    if sum(path) == target:
        result.append(path[:])
        return
    
    if sum(path) > target:  # Prune: can't reach target
        return
    
    for i in range(start, len(nums)):
        path.append(nums[i])
        backtrack(i + 1, path, target)
        path.pop()
```

**Pruning reduces exponential time significantly!**

### 4. Avoid Duplicates in Result

```python
# For combinations/subsets with duplicates:
nums.sort()  # Sort first
for i in range(start, len(nums)):
    if i > start and nums[i] == nums[i-1]:
        continue  # Skip duplicate
    path.append(nums[i])
    backtrack(i + 1, path)
    path.pop()
```

---

## Common Patterns & Complexities

| Problem | Time | Space | Pattern |
|---|---|---|---|
| Permutations | O(n!) | O(n) | All orderings |
| Combinations | O(C(n,k)) | O(k) | Choose k from n |
| Subsets | O(2^n) | O(n) | All subsets |
| N-Queens | O(n!) | O(n) | Place without conflict |
| Sudoku | O(9^(n²)) | O(n²) | Fill valid cells |

---

## Design Checklist

When writing backtracking:

- [ ] **Base case:** When do we stop recursing?
- [ ] **Choice:** What are the possible choices at each step?
- [ ] **Recursion:** Make choice, recurse, backtrack
- [ ] **Undo:** Always undo the choice (pop, remove, etc.)
- [ ] **Copy result:** Use `path[:]` not `path`
- [ ] **Pruning:** Can we cut branches early?
- [ ] **Duplicates:** Do we need to skip duplicates?
- [ ] **Constraints:** Are there constraints to validate?

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forget to backtrack | Always undo: path.pop() after recursion |
| Don't copy result | Use path[:] not path |
| Inefficient start | Use start index to avoid duplicates |
| No pruning | Add early termination when possible |
| Duplicate results | Sort and skip duplicate elements |
| Wrong base case | Make sure you capture all solutions |

---

## Time Complexity Analysis

**Backtracking is exponential!**
- Permutations: O(n!)
- Combinations: O(2^n)
- Subsets: O(2^n)

**With pruning:** Can be significantly better depending on constraint

---

## Interview Tips

1. **Start with brute force:** Understand all possibilities first
2. **Add pruning:** Can we cut branches?
3. **Mention complexity:** It's exponential, be aware
4. **Handle duplicates:** Sort first, skip duplicates
5. **Copy solutions:** Don't use reference, copy list
6. **Explain recursion:** Clear base case and choice
7. **Optimize if possible:** Use pruning, memoization

---

*Tips for solving recursive backtracking problems*
