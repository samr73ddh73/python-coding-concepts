# Great Explanation! https://www.youtube.com/watch?v=-dUiRtJ8ot0
# Reference: https://www.geeksforgeeks.org/dsa/introduction-to-segment-trees-2/

"""
SEGMENT TREE - QUICK REFERENCE

WHAT IS IT?
- A binary tree data structure for storing information about array intervals/segments
- Each node represents a range of the array
- Uses divide-and-conquer approach: array is recursively split until individual elements

WHY USE IT?
- Efficiently handles RANGE QUERIES and POINT/RANGE UPDATES
- Perfect when you need BOTH fast queries AND fast updates
- Alternative to prefix sums (only fast queries) or plain arrays (only fast updates)

WHEN TO USE?
Use segment trees for problems involving:
- Range sum/min/max queries with updates
- Finding GCD, LCM, AND, OR, XOR over ranges
- Counting specific elements in ranges
- Any associative and binary operations on ranges

TIME & SPACE COMPLEXITY:
┌─────────────────┬──────────────┐
│ Operation       │ Complexity   │
├─────────────────┼──────────────┤
│ Build Tree      │ O(n)         │
│ Range Query     │ O(log n)     │
│ Point Update    │ O(log n)     │
│ Range Update*   │ O(log n)     │ *with lazy propagation
│ Space           │ O(4n) ≈ O(n) │
└─────────────────┴──────────────┘

STRUCTURE:
- Array-based representation (0-indexed in this implementation)
- Node i has:
  - Left child: 2*i + 1
  - Right child: 2*i + 2
  - Parent: (i-1)//2
- Size: 4*n (safe upper bound for any n)
- Leaf nodes: individual array elements
- Internal nodes: merged value of children (sum/min/max/etc)

CORE OPERATIONS:

1. BUILD - O(n)
   - Recursively divide array into halves
   - Leaf nodes store individual elements
   - Internal nodes store merged result of children
   - Must define: what to store & how to merge

2. QUERY - O(log n)
   Three cases for range [l, r]:
   - Complete overlap (start>=l and end<=r): return node value
   - No overlap (l>end or r<start): return identity value
   - Partial overlap: recurse on both children and merge

3. UPDATE - O(log n)
   - Navigate to target index
   - Update leaf node
   - Recalculate all parent nodes on path back to root

LAZY PROPAGATION:
- Optimization for range updates
- Delays updates until necessary
- Uses separate lazy[] array to store pending updates
- Push updates down only when visiting nodes
- Maintains O(log n) for range updates

KEY POINTS:
- Operations must be associative and binary
- Merge operation should be O(1) for efficiency
- More space than Fenwick Tree but more flexible
- Can handle any associative operation (Fenwick limited to invertible ops)

IMPLEMENTATION BELOW: Range Maximum Query (RMQ)
"""


class SegmentTree:
    def __init__(self, nums):
        n = len(nums)
        self.seg = [float('-inf') for _ in range(2*n)]
        self.nums = nums
    def build(self, ind, start, end):
        if start == end:
            self.seg[ind] = self.nums[start]
            return 
        mid = (start + end)//2
        self.build(2*ind+1, start, mid)
        self.build(2*ind+2, mid+1, end)
        self.seg[ind] = max(self.seg[2*ind+1], self.seg[2*ind+2])
    
    def query(self, ind, l, r, start, end):
        if start>=l and end <= r:
            return self.seg[ind]
        mid = (start + end)//2
        if l> end or r < start:
            return float('-inf')
        left = self.query(2*ind+1, l, r, start, mid)
        right = self.query(2*ind+2, l, r, mid+1, end)
        return max(left, right)

    def update(self, segInd, ind, val, start, end):
        if start == end:
            self.nums[ind] = val
            self.seg[segInd] = val
        else:
            mid = (start+end)//2 
            if ind <= mid and ind>= start:
                self.update(2*segInd+1, ind, val, start, mid)
            else:
                self.update(2*segInd+2, ind, val, mid+1, end)
            self.seg[segInd] = max(self.seg[2*segInd+1], self.seg[2*segInd+2])   
        
def main():
    nums = [1,2,10,11,6,-1,5,3,4]
    s = SegmentTree(nums)
    s.build(0, 0, len(nums)-1)
    print(s.seg)
    print(s.query(0, 5, 6,0, len(nums)-1))
    s.update(0, 4, 12, 0, len(nums)-1)
    print(s.seg)

main()
