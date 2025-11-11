def lcs(s1: str, s2: str, n: int, m: int ) -> int:
    if (n == 0 or m == 0):
        return 0
    if s1[n-1] == s2[m-1]:
        return 1 + lcs(s1, s2, n-1, m-1)
    return max(lcs(s1, s2, n-1, m), lcs(s1, s2, n, m-1))


def lcsMem(s1: str, s2: str, n: int, m: int, dp ) -> int:
    if (n == 0 or m == 0):
        return 0
    if dp[n][m] != -1:
        return dp[n][m]
    if s1[n-1] == s2[m-1]:
        dp[n][m] = 1 + lcs(s1, s2, n-1, m-1)
    else:
        dp[n][m] =  max(lcs(s1, s2, n-1, m), lcs(s1, s2, n, m-1))
    return dp[n][m]

def lcsBottomup(s1: str, s2: str, n: int, m: int ) -> int:
    dp = [ [0] * (m+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1,m+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[n][m]

def main():
    s1 = 'abcdefghr'
    s2 = 'pppp'
    n = len(s1)
    m = len(s2)
    dp = [ [-1] * (m+1) for _ in range(n+1)]
    print(lcs(s1, s2, len(s1), len(s2)))
    print(lcsMem(s1, s2, len(s1), len(s2), dp))
    print(lcsBottomup(s1, s2, len(s1), len(s2)))

main()

