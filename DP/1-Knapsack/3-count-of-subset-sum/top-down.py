def countOfSubsetSum(arr, targetSum, n, dp):
    if targetSum == 0:  #This seq matters
        return 1
    if n == 0 :
        return 0
    if dp[n][targetSum]!=-1:
        return dp[n][targetSum]
    if arr[n-1] <= targetSum:
        dp[n][targetSum] = countOfSubsetSum(arr, targetSum-arr[n-1], n-1, dp) + countOfSubsetSum(arr, targetSum, n-1, dp)
    else:
        dp[n][targetSum] = countOfSubsetSum(arr, targetSum, n-1, dp)

    return dp[n][targetSum]

def main():
    targetSum = 6
    arr = [1, 2, 3, 3, 4, 8, 2]
    n = len(arr)
    dp = [ [-1] * (targetSum+1) for _ in range(n+1)]
    print(countOfSubsetSum(arr, targetSum, n, dp))

if __name__ == '__main__':
    main()


# NOTE: This is only for non negative integers;