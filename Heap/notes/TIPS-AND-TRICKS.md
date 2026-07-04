# 🎯 Heap Tips & Tricks

> Essential tips for heap/priority queue problems

---

## Key Tips

### Heap Properties

- **Min Heap:** Parent ≤ Children (smallest at root)
- **Max Heap:** Parent ≥ Children (largest at root)
- Python's `heapq` is **min heap** by default
- Complete binary tree (except last level)
- Operations: insert O(log n), extract min O(log n), heapify O(n)

### Using Python's heapq

```python
import heapq

# Min heap
heap = []
heapq.heappush(heap, 5)      # Add element
heapq.heappush(heap, 3)
min_val = heapq.heappop(heap)  # Remove min (3)

# Max heap - use negative values
max_heap = []
heapq.heappush(max_heap, -5)   # Push negative
max_val = -heapq.heappop(max_heap)  # Pop and negate

# Heapify existing list
nums = [5, 3, 8, 1]
heapq.heapify(nums)  # O(n), not O(n log n)

# Get k largest elements
k_largest = heapq.nlargest(k, nums)  # O(n log k)
k_smallest = heapq.nsmallest(k, nums)  # O(n log k)
```

### Common Patterns

| Problem Type | Approach | Time |
|---|---|---|
| K largest elements | Min heap of size k | O(n log k) |
| K smallest elements | Max heap of size k | O(n log k) |
| Median of stream | Min heap + max heap | O(log n) per insert |
| Top k frequent | Min heap by frequency | O(n log k) |
| Schedule tasks | Priority by deadline | O(n log n) |

---

## Key Insights

**Don't sort array for k-largest!**
```python
# Bad: O(n log n)
sorted_nums = sorted(nums, reverse=True)
return sorted_nums[:k]

# Good: O(n log k)
heap = []
for num in nums:
    heapq.heappush(heap, num)
    if len(heap) > k:
        heapq.heappop(heap)
```

**When to heapify vs push:**
- Build heap from scratch: `heapify()` is O(n)
- Add to existing heap: `push()` is O(log n)
- Don't rebuild heap unnecessarily!

**Heap with custom objects:**
```python
# Use tuples - heaps compare element by element
heap = []
heapq.heappush(heap, (priority, item))  # Sorts by priority first

# Or make class comparable
class Task:
    def __lt__(self, other):
        return self.priority < other.priority
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forget Python is min heap | Use negative values for max heap |
| heapify() modifies in-place | Heap gets modified, not sorted array |
| Getting top k inefficiently | Use k-size heap, not full heapify |
| Not understanding heap order | Only parent-child order guaranteed, not siblings |
| Building heap wrong | Use heapify() for O(n), not n pushes O(n log n) |

---

## Time & Space Complexity

| Operation | Time | Space |
|---|---|---|
| Push (heappush) | O(log n) | O(1) |
| Pop (heappop) | O(log n) | O(1) |
| Build heap (heapify) | O(n) | O(1) |
| Access root | O(1) | - |
| K largest (nlargest) | O(n log k) | O(k) |
| Heap sort | O(n log n) | O(1) or O(n) |

---

## Edge Cases

- Single element heap
- All same values
- Duplicate elements
- Negative numbers (for max heap negation)
- Empty heap (pop from empty!)
- Large k (k ≥ heap size)

---

## Interview Tips

1. **When to use heap:**
   - "Find K largest/smallest" → Heap (not sort)
   - "Median of stream" → Two heaps
   - "Top k frequent" → Heap
   - "Priority scheduling" → Heap

2. **Optimize space:** K-size heap vs full array

3. **Implementation choice:** Python `heapq` vs custom

4. **Edge case handling:** Empty heap, k > n, duplicates

---

*Tips for heap data structure and priority queue problems*
