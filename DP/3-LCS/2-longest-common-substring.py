
maxEle = float('-inf')
def lcs(s1: str, s2: str, n, m, res) -> int :
    if (n == 0 or m == 0):
        return res
    if s1[n-1] == s2[m-1]:
        return lcs(s1, s2, n-1, m-1, res+1)
    res =  max(res, lcs(s1, s2, n-1, m, 0), lcs(s1, s2, n, m-1, 0))
    return res

def lcsTopdown(s1: str, s2: str, n, m, dp) -> int:
    global maxEle
    if (n == 0 or m == 0):
        return 0
    if dp[n][m]!= -1:
        return dp[n][m]
    if s1[n-1] == s2[m-1]:
        dp[n][m] = 1 + lcsTopdown(s1, s2, n-1, m-1, dp)
        maxEle = max(maxEle, dp[n][m])
    else:
        dp[n][m] = 0
    lcsTopdown(s1, s2, n-1, m, dp)
    lcsTopdown(s1, s2, n, m-1, dp)
    return maxEle
     
def main():
    s1 = 'abc'
    s2 = 'bcd'
    n = len(s1)
    m = len(s2)
    dp = [ [-1] * (m+1) for _ in range(n+1)]
    print(lcs(s1, s2, len(s1), len(s2), 0))
    print(lcsTopdown(s1, s2, len(s1), len(s2), dp))
    print(dp)

main()