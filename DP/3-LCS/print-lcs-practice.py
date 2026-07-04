class Solution:
    def shortestCommonSupersequence(self, str1: str, str2: str) -> str:
        n, m = len(str1), len(str2)
        dp = [[-1]* m for _ in range(n)]
        lcs = self.lcs(str1, str2, len(str1)-1, len(str2)-1, dp)
        print(dp)
        print(lcs)
    def lcs(self, str1, str2, n, m, dp):
        if n < 0 or m<0:
            return ''
        if dp[n][m]!=-1:
            return dp[n][m]
        if str1[n] == str2[m]:
            dp[n][m] =  self.lcs(str1, str2, n-1, m-1, dp) + str1[n]
            
        else:
            left = self.lcs(str1, str2, n-1, m, dp)
            right = self.lcs(str1, str2, n, m-1, dp)
            finalStr = left if len(left) > len(right) else right
            dp[n][m] = finalStr
        return dp[n][m]

def main():
    str1 = "abac"
    str2 = "cab"
    Solution().shortestCommonSupersequence(str2, str1)

main()