# MERGE INTERVALS - PATTERN GUIDE

## Three Core Patterns

### 1. Sort by Start Time
**When:** Merge overlapping intervals, insert intervals
**Why:** Process intervals in chronological order, merge when current.start ≤ previous.end

**Template:**
```python
intervals.sort(key=lambda x: x[0])
merged = [intervals[0]]
for curr in intervals[1:]:
    if curr[0] <= merged[-1][1]:  # Overlapping
        merged[-1][1] = max(merged[-1][1], curr[1])  # Merge
    else:
        merged.append(curr)
```

**Time:** O(n log n), **Space:** O(n)

---

### 2. Sort by End Time
**When:** Maximum non-overlapping intervals, meeting scheduling, remove minimum intervals

**Why:** Keep interval that ends earliest to leave room for future intervals

**Greedy Strategy:**
- Sort by end time
- Keep first interval
- For next interval: if start ≥ previous end, keep it; else skip

**Template:**
```python
intervals.sort(key=lambda x: x[1])  # Sort by END
count = 1
end = intervals[0][1]

for i in range(1, len(intervals)):
    if intervals[i][0] >= end:  # No overlap
        count += 1
        end = intervals[i][1]
```

**Example:** [[1,3], [2,4], [3,5]]
- Sort by end: [[1,3], [2,4], [3,5]]
- Keep [1,3] (ends earliest)
- [2,4] overlaps (2 < 3), skip
- [3,5] no overlap (3 ≥ 3), keep
- Max non-overlapping = 2

**Time:** O(n log n), **Space:** O(1)

---

### 3. Line Sweep
**When:** Count overlaps, minimum resources needed, max concurrent events

**Why:** Avoid O(n²) checking every pair, use events + prefix sum for O(n log n)

**Core Idea:**
- Convert intervals to events: start → +1, end → -1
- Sort events by time
- Calculate prefix sum to track overlap count

**Template:**
```python
events = {}
for start, end in intervals:
    events[start] = events.get(start, 0) + 1
    events[end] = events.get(end, 0) - 1

max_overlap = 0
current = 0
for time in sorted(events.keys()):
    current += events[time]
    max_overlap = max(max_overlap, current)
```

**Time:** O(n log n), **Space:** O(n)

---

## Pattern Decision Tree

```
Question: What do you need?

├─ Merge/combine overlapping intervals → Sort by START
├─ Maximum non-overlapping intervals → Sort by END
├─ Count overlaps / min resources → Line Sweep
└─ Insert interval → Sort by START
```

---

## Common Problems by Pattern

| Problem | Pattern | Key |
|---------|---------|-----|
| Merge Intervals | Start | Merge when overlap |
| Insert Interval | Start | Insert + merge |
| Non-overlapping Intervals | End | Greedy: keep earliest end |
| Meeting Rooms II | Line Sweep | Count max concurrent |
| My Calendar | Line Sweep | Track overlaps |
| Car Pooling | Line Sweep | Passengers on/off |

---

## Key Insights

**Sort by End Time** = Greedy for maximizing count
- Keep interval ending first = leave room for more

**Line Sweep** = Avoid O(n²) pairwise checks
- Events + prefix sum = O(n log n)

**Overlap Check:**
- `a.start <= b.end and b.start <= a.end` (general)
- If sorted by start: `curr.start <= prev.end`
