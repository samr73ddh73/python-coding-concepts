#https://leetcode.com/problems/coin-change-ii/

class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        dp = [[-1]* (len(coins)+1) for _ in range(amount +1)]
        return self._change(amount, coins, len(coins), dp)
    def _change(self, amount: int, coins: List[int], n: int, dp: List[List[int]]) -> int: 
        if amount == 0:
            return 1
        if n == 0:
            return 0
        if dp[amount][n] != -1:
            return dp[amount][n]
        take = 0
        if coins[n-1] <= amount:
            take = self._change(amount-coins[n-1], coins, n, dp)
        skip = self._change(amount, coins, n-1, dp)
        dp[amount][n] = take + skip
        return dp[amount][n]
        
        