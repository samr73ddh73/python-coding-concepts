1. Normal Binary Serach
2. Binary Search on Answers:
    
- The #1 signal for binary search on answer problems is this phrasing pattern:
    Find the minimum X such that [some condition] is possible"
    or
    "Find the maximum X such that [some condition] holds"

    In this problem: "Find the minimum capacity such that all packages can be shipped within D days."
    That's the tell. You're not searching an array — you're searching the answer space.


No worries, I know this problem well. Let me break down the intuition deeply.

---

## The Core Intuition: "Minimum/Maximum that satisfies a condition"

The **#1 signal** for binary search on answer problems is this phrasing pattern:

> **"Find the minimum X such that [some condition] is possible"**
> or
> **"Find the maximum X such that [some condition] holds"**

In this problem: *"Find the **minimum capacity** such that all packages can be shipped within D days."*

That's the tell. You're not searching an array — you're **searching the answer space**.

---

## The 3-Question Framework

When you see a problem, ask yourself these:

**1. Can I define a search space with a clear low and high bound?**

For this problem:
- `low = max(weights)` — the ship must at least carry the heaviest package
- `high = sum(weights)` — worst case, ship everything in one day

So the answer lives somewhere in `[max(weights), sum(weights)]`. That's a well-defined range → binary search is viable.

**2. Is the predicate function monotonic?**

Define `canShip(capacity, D)` = "can we ship all packages within D days at this capacity?"

Ask: if `canShip(10)` is `True`, is `canShip(11)` also `True`? **Yes, always.** More capacity never hurts.

This means the search space looks like:

```
capacity:   7   8   9   10  11  12  ...  sum
canShip:    F   F   F   T   T   T   ...  T
```

There's a **clean False → True transition**. Binary search finds that boundary in O(log N).

**3. Is brute force too slow?**

Checking every capacity from `max(weights)` to `sum(weights)` linearly would be O(sum × N). Binary search brings it to O(N log(sum)).

---

## The Pattern Family

Once you internalize this, you'll recognize the whole family:

| Problem | Search Space | Monotonic Predicate |
|---|---|---|
| Capacity to Ship (this one) | `[max(w), sum(w)]` | canShip(cap) |
| Koko Eating Bananas | `[1, max(piles)]` | canFinish(speed) |
| Find Minimum in Rotated Array | indices | — |
| Split Array Largest Sum | `[max(arr), sum(arr)]` | canSplit(limit) |
| Magnetic Force Between Balls | `[1, max_dist]` | canPlace(dist) |

Notice the last three have **identical search space structure** to this problem. They're the same problem dressed differently.

---

## The Keyword Radar

Train yourself to spot these words in problem statements:

- **"minimum/maximum"** + **"such that"** or **"at least/most"**
- **"within K days/operations/moves"**
- **"feasible"**, **"possible"**, **"can you achieve"**
- Constraints where brute force on the answer is O(N²) or worse

---

## The Mental Model

Think of it this way: instead of searching for an element *in* a data structure, you're searching for a **threshold** on a number line where the world flips from "impossible" to "possible." Binary search is just a fast way to find any such threshold.

> Every time you see *"minimize the maximum"* or *"maximize the minimum"* — that's almost always binary search on answer.

Once this clicks, problems like this become very mechanical: define bounds → write `canDoIt(mid)` → binary search on it.