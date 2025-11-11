from typing import List, Dict, Tuple

def countOfSubsetSum(nums: List[int], targetSum: int, n: int, dp: Dict[Tuple[int, int], int]) -> int:
    if targetSum == 0:
        return 1
    if n == 0:
        return 0
    if (n, targetSum) in dp:
        return dp[(n, targetSum)]
    if nums[n-1] <= targetSum:
        dp[(n, targetSum)] = countOfSubsetSum(nums, targetSum-nums[n-1], n-1, dp) + countOfSubsetSum(nums, targetSum, n-1, dp)
    else:
        dp[(n, targetSum)] = countOfSubsetSum(nums, targetSum, n-1, dp)
    return dp[(n, targetSum)]

def main():
    targetSum = 6
    arr = [1, 0, 6, 8, -2]
    n = len(arr)
    dp:Dict[Tuple[int, int]] = {}
    print(countOfSubsetSum(arr, targetSum, n, dp))

if __name__ == '__main__':
    main()
