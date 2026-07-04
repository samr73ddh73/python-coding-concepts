By looking at the constraints of a problem, we can often "guess" the solution.

Common time complexities (trick: O(x) should be less that 10^8)

toh agar n is
1. 10^8, so, time complexity can be n or less
2. 10^6 hai, toh <= nlogn
3. 10^4 , toh < n^2 (kyunking, (10^4)^2 = 10^8)

Let n be the main variable in the problem.

If n ≤ 12, the time complexity can be O(n!).
If n ≤ 25, the time complexity can be O(2n).
If n ≤ 100, the time complexity can be O(n4).
If n ≤ 500, the time complexity can be O(n3).
If n ≤ 104, the time complexity can be O(n2).
If n ≤ 106, the time complexity can be O(n log n).
If n ≤ 108, the time complexity can be O(n).
If n > 108, the time complexity can be O(log n) or O(1)


Time complexity of recusrion:
1. TC = word done by one node * total number of nodes in recursive tree
   total number of nodes in recursive tree = depth(nodes at each level)

   ex: ek binary tree me, with depth as h, 
   # of nodes: 1 + 2 + 4 + 8 ... 2^h = 2^(h+1) -1
   
