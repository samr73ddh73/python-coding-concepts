def subsetSum(arr, sum, n):
    if(sum == 0):
        return True
    elif n == 0:
        return False
    if arr[n-1] <= sum:
        return (subsetSum(arr, sum-arr[n-1], n-1)
        or subsetSum(arr, sum, n-1))
    return subsetSum(arr, sum, n-1)

def main():
    sum = 12
    arr = [2, 3, 4, 7, 8, 10]
    print(subsetSum(arr, sum, 6))

if __name__ == '__main__':
    main()


Time complexity: 2^n
Space complexity: Stack space. (how much?)