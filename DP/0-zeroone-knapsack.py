class Solution:
    def __init__(self):
        mem: Dict[Tuple[int, int], int] = {}
    def knapsack(wt: List[int], profit: List[int], n: int, cap: int):
        if(cap <= 0 or n ==0 ):
            return 0
        if(mem[tuple[cap, n]]):
            return mem[tuple[cap, n]]
        take = 0
        if(wt[n-1] <= cap):
            take = knapsack(wt, profit, n-1, cap-wt[n-1]) + profit[n-1]
        skip = knapsack(wt, profit, n-1, cap)
        mem[tuple[cap, n]] = max(take, skip)
        return mem[tuple[cap, n]]
    def main():
        wt = [3, 1, 5, 2]
        profit = [23, 37, 52, 1]
        cap = 7
        n = len(wt)
        print(knapsack(wt: List[int], profit: List[int], n: int, cap: int))

