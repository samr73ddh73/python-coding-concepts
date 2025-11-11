https://leetcode.com/problems/partition-equal-subset-sum/description/

class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        if(sum(nums) % 2 !=0):
            return False
        targetSum = sum(nums)//2
        n = len(nums)
        dp = [[-1]* (targetSum+1) for _ in range(n+1)]
        return self._canPartition(nums, targetSum, len(nums), dp)
    def _canPartition(self, arr: List[int], targetSum, n, dp ):
        if targetSum == 0:
            return True
        if n == 0:
            return False
        if dp[n][targetSum]!= -1:
            return dp[n][targetSum]
        if arr[n-1] <= targetSum:
            dp[n][targetSum] = (self._canPartition(arr, targetSum- arr[n-1], n-1, dp ) or
             self._canPartition(arr, targetSum, n-1, dp ))
        else:
            dp[n][targetSum] =  self._canPartition(arr, targetSum, n-1, dp )
        return dp[n][targetSum]
        