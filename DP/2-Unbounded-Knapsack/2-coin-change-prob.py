class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [[-1]* (amount+1) for _ in range(len(coins)+1)]
        res = self._coinChange(coins, amount, len(coins), dp)
        if res == float('inf'):
            return -1
        return res
    def _coinChange(self, coins, amount, n, dp):
        if amount == 0:
            return 0
        if n == 0:
            return float('inf')
        if dp[n][amount]!=-1:
            return dp[n][amount]
        if coins[n-1] <= amount:
            dp[n][amount] = min(
               1 + self._coinChange(coins, amount-coins[n-1], n, dp),
                self._coinChange(coins, amount, n-1, dp )
            )
        else:
            dp[n][amount] =  self._coinChange(coins, amount, n-1, dp )
        return dp[n][amount]