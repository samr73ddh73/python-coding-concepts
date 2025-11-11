minEle = 10000
def minSubsetSumDiff(arr, targetSum, n):
    if n == 0 or targetSum == 0:
        return minEle
    subset1 = targetSum
    subset2 = sum(arr) - subset1
    minEle = min(minEle, abs(subset2-subset1))
    print(minEle)
    return min(minSubsetSumDiff(arr, targetSum - arr[n-1], n-1 ),
    minSubsetSumDiff(arr, targetSum, n-1 ) )

def main():
    arr = [1, 6, 11, 5]
    print(minSubsetSumDiff(arr, sum(arr), len(arr)))

main()


S

s1 + s2 = S
s1-(S-s1)
2s1- S  => Minimise

