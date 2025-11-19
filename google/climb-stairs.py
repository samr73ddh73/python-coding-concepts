
def climbStairs( n: int) -> int:
    dp = [-1 for _ in range(n+1)]
    return helper(n, dp)

def helper( n, dp):
    if n == 0:
        dp[n] = 1
    if n < 0:
        return 0
    if dp[n]!= -1:
        return dp[n]
    dp[n] = helper(n-1) + helper(n-2)
    return dp[n]

def main():
    n = 10
    print(climbStairs(n))

main()