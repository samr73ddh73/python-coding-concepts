from typing import List
def rodCutting(rodLength: int, profits: List[int], n: int, dp: List[List[int]]) -> int:
    for i in range(1, rodLength+1):
        for j in range(1, rodLength+1):
            dp[i][j] = max(profits[i-1] + dp[i][j-i], dp[i-1][j])
    return dp[rodLength][n]

def main():
    arr = [1,5,8,9,10, 17,17,20]
    dp = [ [0]* (len(arr)+1) for _ in range(len(arr)+1)]
    print(rodCutting(len(arr), arr, len(arr), dp))

main()