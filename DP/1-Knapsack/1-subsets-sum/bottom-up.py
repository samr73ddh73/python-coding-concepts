def subsetSum(arr, targetSum, n):
    dp = [ [False]*(targetSum+1) for _ in range(n+1)] #n, targetSum
    for i in range(n+1):
        dp[i][0] = True
    for i in range(1, targetSum+1):
        dp[0][i] = False
    for i in range (1, n+1):
        for j in range(1, targetSum+1):
            if arr[i-1] <= j:
                dp[i][j] = dp[i-1][j-arr[i-1]] or dp[i-1][j]
            else:
                dp[i][j] = dp[i-1][j]
    return dp[n][targetSum]

def main():
    targetSum = 121
    arr = [2, 3, 4, 7, 8, 10]
    print(subsetSum(arr, targetSum, len(arr)))

if __name__ == '__main__':
    main()
