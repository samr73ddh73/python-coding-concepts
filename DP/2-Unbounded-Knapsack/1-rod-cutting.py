from typing import List
def rodCutting(rodLength: int, profits: List[int], n: int, dp: List[List[int]]) -> int:
    if rodLength <= 0 or n <= 0:
        return 0
    # print (n, rodLength)
    if dp[n][rodLength] != -1:
        return dp[n][rodLength]
    dp[n][rodLength] = max(
        profits[n-1] + rodCutting(rodLength-n, profits, n, dp),
        rodCutting(rodLength, profits, n-1, dp)
    )
    return dp[n][rodLength]

def main():
    dp = [ [-1]* 9 for _ in range(9)]
    print(rodCutting(8, [1,5,8,9,10, 17,17,20], 8, dp))

main()