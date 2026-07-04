class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        dp = [[-1]* len(p) for _ in range(len(s))]
        return self._isMatch(s,p,len(s)-1,len(p)-1, dp)
        
    def _isMatch(self, s, p, n, m, dp):
        if n <0 and m<0:
            return True
        if n <0 and m >=0:
            while m >=0:
                if p[m] != '*':
                    return False
                m -= 1
            return True
        if n < 0 or m <0:
            return False
        if dp[n][m]!= -1:
            return dp[n][m]
        if s[n] == p[m] or p[m] == '?':
            dp[n][m] = self._isMatch(s, p, n-1, m-1, dp)
        elif p[m] == '*':
            dp[n][m] = self._isMatch(s,p, n, m-1, dp) or self._isMatch(s,p,n-1,m, dp)
        elif s[n] != p[m]:
            dp[n][m] = False
        return dp[n][m]

def main():
    print(Solution().isMatch('aabcbcbcde', '*'))

main()