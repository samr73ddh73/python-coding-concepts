# 🎯 Greedy Algorithm Tips & Tricks

> Patterns and insights for greedy algorithm problems

---

## Core Concept

**Greedy = Make locally optimal choice at each step**

Hope this leads to globally optimal solution. Not always correct - must **prove greedy works!**

---

## When Greedy Works

### 1. Greedy Choice Property
- Making locally optimal choice doesn't prevent global optimum

### 2. Optimal Substructure
- Solution contains optimal solutions of subproblems

**Test:** Can we exchange optimal choices with greedy ones without worse result?

---

## Common Greedy Patterns

### Pattern 1: Activity Selection

```python
# Select maximum non-overlapping activities
def selectActivities(activities):  # (start, end) tuples
    # Sort by end time (greedy: earliest finish)
    activities.sort(key=lambda x: x[1])
    
    selected = [activities[0]]
    for i in range(1, len(activities)):
        if activities[i][0] >= selected[-1][1]:
            selected.append(activities[i])
    
    return selected
```

**Greedy Choice:** Always pick activity that finishes earliest!

### Pattern 2: Interval/Meeting Rooms

```python
# Minimum meeting rooms needed
def minMeetingRooms(intervals):
    events = []
    for start, end in intervals:
        events.append((start, 1))      # +1 room
        events.append((end, -1))       # -1 room
    
    events.sort()
    current_rooms = max_rooms = 0
    for time, delta in events:
        current_rooms += delta
        max_rooms = max(max_rooms, current_rooms)
    
    return max_rooms
```

**Greedy:** Track simultaneous overlaps at each time point

### Pattern 3: Fractional Knapsack

```python
# Maximize value with weight limit
def fractionalKnapsack(items, capacity):  # (value, weight)
    # Sort by value/weight ratio (greedy: most valuable per unit)
    items.sort(key=lambda x: x[0] / x[1], reverse=True)
    
    total_value = 0
    for value, weight in items:
        if weight <= capacity:
            total_value += value
            capacity -= weight
        else:
            total_value += value * (capacity / weight)
            capacity = 0
            break
    
    return total_value
```

**Greedy Choice:** Pick items by best value-to-weight ratio!

### Pattern 4: Jump Game

```python
# Can we reach the end?
def canJump(nums):
    farthest = 0
    for i in range(len(nums)):
        if i > farthest:
            return False
        farthest = max(farthest, i + nums[i])
        if farthest >= len(nums) - 1:
            return True
    return False
```

**Greedy:** Track farthest reachable position

---

## Key Insights

### Greedy Doesn't Always Work!

```python
# Example: Coin change (NOT greedy for all cases)
coins = [1, 3, 4]
amount = 6

# Greedy (wrong): 4 + 1 + 1 = 3 coins
# Optimal (correct): 3 + 3 = 2 coins

# Solution: Use DP, not greedy!
```

### When to Suspect Greedy Works

- "Maximum" or "minimum" objective
- Non-overlapping intervals
- Earliest/latest time problems
- Fractional problems (can take partial items)
- Safe to "use up" resource (no backtracking)

---

## Greedy Algorithms

| Algorithm | Problem | Greedy Choice |
|---|---|---|
| Activity Selection | Select max non-overlapping | Finish earliest |
| Huffman Coding | Optimal prefix-free code | Merge smallest frequency |
| Dijkstra | Shortest path | Nearest unvisited node |
| Kruskal/Prim | Minimum spanning tree | Lightest edge |
| Fractional Knapsack | Maximize value | Best value/weight ratio |
| Interval Scheduling | Meeting rooms | Process by start time |
| Jump Game | Can reach end | Track farthest position |

---

## Design Approach

**To solve a greedy problem:**

1. **Identify the decision:** What choice do we make?
2. **Define greedy strategy:** What's locally optimal?
3. **Prove correctness:** Why does greedy work?
4. **Code the solution:** Implement the choice
5. **Complexity analysis:** Usually O(n log n) for sorting

---

## Time Complexities

| Problem | Time | Notes |
|---|---|---|
| Activity Selection | O(n log n) | Sorting by end time |
| Interval Scheduling | O(n log n) | Sorting events |
| Huffman Coding | O(n log n) | Building tree |
| Dijkstra | O((V+E) log V) | With min-heap |
| Kruskal | O(E log E) | Sorting edges |
| Jump Game | O(n) | Single pass |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Assume greedy always works | Prove it first! |
| Wrong greedy choice | Test with counter-examples |
| Forget to sort | Many problems need sorting first |
| Incorrect proof | Can greedy fail in any case? |
| Overlook edge cases | Empty, single element, etc. |

---

## Interview Tips

1. **Don't assume greedy works** - Verify first!
2. **Counter-examples are powerful** - Show when greedy fails
3. **Prove your choice** - Why is it optimal?
4. **Compare with DP** - When to use which?
5. **Greedy works for:** Interval, activity, fractional problems
6. **Greedy fails for:** Coin change (non-unit), general knapsack
7. **Complexity:** Usually O(n log n) due to sorting

---

*Tips for recognizing and solving greedy algorithm problems*
