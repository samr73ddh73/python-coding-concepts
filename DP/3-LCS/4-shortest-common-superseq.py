def lcs_length(s1: str, s2: str, i: int, j: int, dp) -> str :
    if i == 0 or j == 0:
        return 0
    if dp[i][j] != -1:
        return dp[i][j]
    
    if s1[i-1] == s2[j-1]:
        dp[i][j] = 1 + lcs_length(i-1, j-1)
    else:
        dp[i][j] = max(lcs_length(i-1, j), lcs_length(i, j-1))
    return dp[i][j]


def main():
    s1 = 'geek'
    s2 = 'eke'
    n = len(s1)
    m = len(s2)
    dp = [ [''] * (m+1) for _ in range(n+1)]
    x = lcs_length(s1, s2, len(s1), len(s2), dp)
    result = []
    i, j = n, m
    while i > 0 and j > 0:
        if s1[i-1] == s2[j-1]:
            result.append(s1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            result.append(s1[i-1])
            i -= 1
        else:
            result.append(s2[j-1])
            j -= 1
    
    while i > 0:
        result.append(s1[i-1])
        i -= 1
    while j > 0:
        result.append(s2[j-1])
        j -= 1
    
    return ''.join(reversed(result))

        
print(main())
    