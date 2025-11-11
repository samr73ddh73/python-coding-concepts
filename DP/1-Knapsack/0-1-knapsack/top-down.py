from typing import List, Tuple, Dict
class Solution:
    def __init__(self):
        self.mem: Dict[Tuple[int, int], int] = {}
    def knapsack(self, wt: List[int], profit: List[int], n: int, cap: int):
        if(cap <= 0 or n ==0 ):
            return 0
        if((cap, n) in self.mem):
            return self.mem[tuple[cap, n]]
        take = 0
        if(wt[n-1] <= cap):
            take = self.knapsack(wt, profit, n-1, cap-wt[n-1]) + profit[n-1]
        skip = self.knapsack(wt, profit, n-1, cap)
        self.mem[tuple[cap, n]] = max(take, skip)
        return self.mem[tuple[cap, n]]
    def main(self):
        wt = [3, 1, 5, 2]
        profit = [23, 37, 52, 1]
        cap = 7
        n = len(wt)
        print(self.knapsack(wt, profit, n, cap))

Solution().main()



#time complexity: O(n* capacity)
# space: O(n* capacity) + O(stack size)
