# def subsetSum(arr, n, sum, dp):
#     if(sum == 0):
#         return True
#     if(n == 0):
#         return False
#     # print(dp)
#     if((sum, n) in dp):
#        
#         return dp[tuple[sum, n]]
#     if(arr[n-1]<=sum):
#         dp[tuple[sum, n]] = (subsetSum(arr, n-1, sum-arr[n-1], dp) or
#         subsetSum(arr, n-1, sum, dp))
#     else:
#         dp[tuple[sum, n]] = subsetSum(arr, n-1, sum, dp)

def subsetSum1(arr, n, sum, dp):
    if(sum == 0):
        return True
    if(n == 0):
        return False
    if(dp[sum][n]!=-1):
        return dp[sum][n]
    if(arr[n-1]<=sum):
        dp[sum][n] = (subsetSum1(arr, n-1, sum-arr[n-1], dp) or
        subsetSum1(arr, n-1, sum, dp))
    else:
        dp[sum][n] = subsetSum1(arr, n-1, sum, dp)
    return dp[sum][n]

def main():
    sum = 111
    arr = [2, 3, 4, 7, 10]
    n = len(arr)
    dp = [ [-1]* (n+1) for _ in range(sum+1)]
    print(subsetSum1(arr, n, sum, dp))

if __name__ == '__main__':
    main()


# Time: O(sum*n)
# space: O(sum*n) + stack