def lcs(s1, s2, n, m, dp):
    if ( n == 0 or m == 0):
        return ''
    if dp[n][m]!= -1:
        return dp[n][m]
    if s1[n-1] == s2[m-1]:
        dp[n][m] =  lcs(s1, s2, n-1, m-1, dp) + s1[n-1]
    else:
        c1 = lcs(s1, s2, n-1, m, dp)
        c2 = lcs(s1, s2, n, m-1, dp)
        longerStr = c1 if len(c1) > len(c2) else c2
        dp[n][m] = longerStr
    return dp[n][m]

def main():
    s1 = 'abcfghyi'
    s2 = 'bcdyi'
    n = len(s1)
    m = len(s2)
    dp = [ [-1] * (m+1) for _ in range(n+1)]
    dp[0] = ['' for _ in range(m+1)]
    for i in range(n+1):
        dp[i][0] = ''
    print(lcs(s1, s2, len(s1), len(s2), dp))

# main()

# The above approach has issues:
# 1. creating new string everytime is O(L) operation, because python creates a new string everytime instead of concatenation
# 2. What we can do is, store length and then backtrack

def _lcsEfficient(s1: str, s2: str, n: int, m: int, dp) -> int :
    if ( n == 0 or m == 0):
        return 0
    if dp[n][m]!= -1:
        return dp[n][m]
    if s1[n-1] == s2[m-1]:
        dp[n][m] =  _lcsEfficient(s1, s2, n-1, m-1, dp) + 1
    else:
        dp[n][m] = max(_lcsEfficient(s1, s2, n-1, m, dp), _lcsEfficient(s1, s2, n, m-1, dp))
    return dp[n][m]

def printLcsString(s1, s2):
    n, m = len(s1), len(s2)
    dp = [[-1]* (m+1) for _ in range(n+1)]
    res = []
    _lcsEfficient(s1, s2, n, m, dp)
    i, j = n,m
    while(i>0 and j>0):
        if s1[i-1] == s2[j-1]:
            res.append(s1[i-1])
            print(res)
            i = i-1
            j = j-1
        elif dp[i-1][j] > dp[i][j-1]:
            i = i-1
        else:
            j = j-1
    print(res)
    return ''.join(reversed(res))

print(printLcsString('abcsd', 'bsd'))




