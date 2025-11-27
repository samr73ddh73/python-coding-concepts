"""
================================================================================
PATTERN: Line Sweep Algorithm (Sweep Line)
================================================================================

CONCEPT:
Imagine a vertical line sweeping across the x-axis from left to right.
At each critical point (start/end of interval), we track changes in state.

KEY IDEA:
Instead of processing entire intervals, we process EVENTS at specific points:
- START event: +1 (something begins)
- END event: -1 (something ends)

Then calculate PREFIX SUM to find overlaps at any point in time.

================================================================================
WHY LINE SWEEP?
================================================================================

PROBLEM: Find maximum overlap of intervals
Intervals: [[1,3], [2,5], [4,6]]

NAIVE APPROACH: O(n²)
- For each point in time, count how many intervals cover it
- Check all n intervals for each time point

LINE SWEEP APPROACH: O(n log n)
- Mark start/end points as events
- Sort events by time
- Calculate running count (prefix sum)

================================================================================
CORE TECHNIQUE: EVENT-BASED + PREFIX SUM
================================================================================

Step 1: Convert intervals to events
Intervals: [[1,3], [2,5], [4,6]]

Events:
1: +1 (interval starts)
2: +1 (interval starts)
3: -1 (interval ends)
4: +1 (interval starts)
5: -1 (interval ends)
6: -1 (interval ends)

Step 2: Calculate prefix sum (running count)
Time:  1   2   3   4   5   6
Event: +1  +1  -1  +1  -1  -1
Count:  1   2   1   2   1   0
        ↑   ↑       ↑
     overlap overlap overlap

Max overlap = 2 (at time 2 and 4)

================================================================================
IMPLEMENTATION PATTERNS
================================================================================

PATTERN 1: Using SortedDict (for dynamic updates)
"""

from sortedcontainers import SortedDict

class LineSweepDynamic:
    """
    Use when intervals are added/removed dynamically
    TIME: O(n log n) per operation where n = number of events
    SPACE: O(n)
    """
    def __init__(self):
        self.events = SortedDict()  # time -> count change

    def add_interval(self, start, end):
        # Mark start and end events
        self.events[start] = self.events.get(start, 0) + 1
        self.events[end] = self.events.get(end, 0) - 1

    def get_max_overlap(self):
        max_overlap = 0
        current_overlap = 0

        # Calculate prefix sum
        for count_change in self.events.values():
            current_overlap += count_change
            max_overlap = max(max_overlap, current_overlap)

        return max_overlap


"""
PATTERN 2: Using Array Sorting (for static intervals)
"""

def max_overlap_static(intervals):
    """
    Use when all intervals known upfront
    TIME: O(n log n) - sorting dominates
    SPACE: O(n)
    """
    events = []

    # Create events for all intervals
    for start, end in intervals:
        events.append((start, 1))   # Start event
        events.append((end, -1))    # End event

    # Sort by time (if same time, process ends before starts)
    events.sort(key=lambda x: (x[0], x[1]))

    max_overlap = 0
    current_overlap = 0

    for time, delta in events:
        current_overlap += delta
        max_overlap = max(max_overlap, current_overlap)

    return max_overlap


"""
PATTERN 3: Using Dictionary + Sorting (most common)
"""

def line_sweep_template(intervals):
    """
    General template for line sweep problems
    """
    event_map = {}

    # Step 1: Mark events
    for start, end in intervals:
        event_map[start] = event_map.get(start, 0) + 1
        event_map[end] = event_map.get(end, 0) - 1

    # Step 2: Sort events by time
    sorted_events = sorted(event_map.items())

    # Step 3: Calculate prefix sum and find answer
    current_count = 0
    max_count = 0

    for time, delta in sorted_events:
        current_count += delta
        max_count = max(max_count, current_count)

    return max_count


"""
================================================================================
REAL PROBLEM: My Calendar Two (Triple Booking)
================================================================================

PROBLEM: Allow at most double booking (reject triple booking)
"""

class MyCalendarTwo:
    """
    Line sweep with rollback on triple booking
    TIME: O(n²) worst case (n bookings × n events to check)
    SPACE: O(n)
    """
    def __init__(self):
        self.events = SortedDict()
        self.max_allowed = 2  # Allow double booking only

    def book(self, start, end):
        # Tentatively add booking
        self.events[start] = self.events.get(start, 0) + 1
        self.events[end] = self.events.get(end, 0) - 1

        # Check if triple booking occurs
        current_overlap = 0

        for delta in self.events.values():
            current_overlap += delta

            if current_overlap > self.max_allowed:
                # Rollback - remove this booking
                self.events[start] -= 1
                self.events[end] += 1

                # Cleanup zero entries
                if self.events[start] == 0:
                    del self.events[start]
                if self.events[end] == 0:
                    del self.events[end]

                return False  # Reject booking

        return True  # Accept booking


"""
================================================================================
COMMON VARIATIONS
================================================================================

1. MEETING ROOMS II (LeetCode 253)
   Find minimum number of meeting rooms needed

2. MY CALENDAR I/II/III (LeetCode 729/731/732)
   Allow at most k overlapping bookings

3. CAR POOLING (LeetCode 1094)
   Track passengers getting on/off at stops

4. EMPLOYEE FREE TIME (LeetCode 759)
   Find common free time across all employees

5. NUMBER OF FLOWERS IN FULL BLOOM (LeetCode 2251)
   Count flowers blooming at each time

================================================================================
EXAMPLE 1: Meeting Rooms II
================================================================================
"""

def min_meeting_rooms(intervals):
    """
    Find minimum meeting rooms needed
    TIME: O(n log n)
    SPACE: O(n)
    """
    events = {}

    for start, end in intervals:
        events[start] = events.get(start, 0) + 1  # Meeting starts
        events[end] = events.get(end, 0) - 1      # Meeting ends

    max_rooms = 0
    current_rooms = 0

    # Process events in time order
    for time in sorted(events.keys()):
        current_rooms += events[time]
        max_rooms = max(max_rooms, current_rooms)

    return max_rooms


"""
TRACE:
Meetings: [[0,30], [5,10], [15,20]]

Events:
0: +1  (meeting 1 starts)
5: +1  (meeting 2 starts)
10: -1 (meeting 2 ends)
15: +1 (meeting 3 starts)
20: -1 (meeting 3 ends)
30: -1 (meeting 1 ends)

Prefix sum:
Time:  0   5   10  15  20  30
Rooms: 1   2   1   2   1   0
       ↑   ↑       ↑
Need 2 rooms (at time 5 and 15)

Answer: 2 rooms needed
"""


"""
================================================================================
EXAMPLE 2: Car Pooling
================================================================================
"""

def car_pooling(trips, capacity):
    """
    trips[i] = [numPassengers, from, to]
    Return True if possible to pick up all passengers

    TIME: O(n log n)
    SPACE: O(n)
    """
    events = {}

    for passengers, start, end in trips:
        events[start] = events.get(start, 0) + passengers  # Pick up
        events[end] = events.get(end, 0) - passengers      # Drop off

    current_passengers = 0

    for location in sorted(events.keys()):
        current_passengers += events[location]

        if current_passengers > capacity:
            return False  # Exceeds capacity

    return True


"""
TRACE:
trips = [[2,1,5], [3,3,7]]
capacity = 4

Events:
1: +2 (pick up 2)
3: +3 (pick up 3)
5: -2 (drop off 2)
7: -3 (drop off 3)

At location 3: current = 2 + 3 = 5 > 4 ❌
Answer: False (exceeds capacity)
"""


"""
================================================================================
WHEN TO USE LINE SWEEP
================================================================================

✓ Multiple overlapping intervals
✓ Need to find max overlap / min resources
✓ Events occur at discrete time points
✓ Want O(n log n) instead of O(n²)

RECOGNITION PATTERNS:
- "Maximum number of overlapping..."
- "Minimum resources needed..."
- "At most k overlaps allowed..."
- "Count at each time point..."

================================================================================
TEMPLATE DECISION TREE
================================================================================

Question: Are intervals added dynamically?
│
├─ YES → Use SortedDict
│   │    - My Calendar problems
│   │    - Real-time booking systems
│   │
│   └─ Time: O(n) per query, Space: O(n)
│
└─ NO → Use Array + Sort
    │    - Meeting Rooms
    │    - Car Pooling
    │    - Static interval problems
    │
    └─ Time: O(n log n), Space: O(n)

================================================================================
KEY DIFFERENCES FROM OTHER APPROACHES
================================================================================

| Approach | Time | When to Use |
|----------|------|-------------|
| Brute Force | O(n²) | Never in interviews |
| Line Sweep | O(n log n) | Overlapping intervals |
| Merge Intervals | O(n log n) | Combine overlaps |
| Interval Tree | O(n log n) | Dynamic queries |

LINE SWEEP vs MERGE INTERVALS:
- Line sweep: Count/track overlaps at each point
- Merge: Combine overlapping intervals into one

================================================================================
COMMON MISTAKES
================================================================================

❌ Forgetting to handle events at same time
   - Process END events before START events at same time

❌ Not using SortedDict for dynamic problems
   - Regular dict doesn't maintain order!

❌ Deleting wrong key during rollback
   - Check what you're deleting carefully

❌ Returning inside the loop too early
   - Make sure return is properly indented

================================================================================
FANG INTERVIEW TIPS
================================================================================

1. "I recognize this as overlapping intervals → Line sweep approach"

2. "I'll mark start as +1, end as -1, then calculate prefix sum"

3. "Using SortedDict for O(log n) insertion while maintaining sorted order"

4. "Time: O(n log n) for sorting events, Space: O(n) for event storage"

5. "Alternative: Could use Interval Tree for O(log n) queries"

6. Mention: "This avoids O(n²) brute force checking every interval pair"
"""

# Example usage and tests
if __name__ == "__main__":
    print("=== Max Overlap Example ===")
    intervals = [[1,3], [2,5], [4,6]]
    print(f"Intervals: {intervals}")
    print(f"Max overlap: {max_overlap_static(intervals)}")  # 2

    print("\n=== Meeting Rooms Example ===")
    meetings = [[0,30], [5,10], [15,20]]
    print(f"Meetings: {meetings}")
    print(f"Min rooms needed: {min_meeting_rooms(meetings)}")  # 2

    print("\n=== Car Pooling Example ===")
    trips = [[2,1,5], [3,3,7]]
    capacity = 4
    print(f"Trips: {trips}, Capacity: {capacity}")
    print(f"Possible: {car_pooling(trips, capacity)}")  # False

    print("\n=== My Calendar Two Example ===")
    calendar = MyCalendarTwo()
    print(f"Book [10,20]: {calendar.book(10, 20)}")  # True
    print(f"Book [50,60]: {calendar.book(50, 60)}")  # True
    print(f"Book [10,40]: {calendar.book(10, 40)}")  # True (double booking)
    print(f"Book [5,15]: {calendar.book(5, 15)}")   # False (triple booking)
