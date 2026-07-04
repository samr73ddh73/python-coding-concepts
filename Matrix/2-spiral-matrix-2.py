# https://leetcode.com/problems/spiral-matrix-ii/
from typing import List

class Solution:
    def generateMatrix(self, n: int) -> List[List[int]]:
        res = [[0]* n for _ in range(n)]
        left, right = 0, n-1
        top, bottom = 0, n-1
        i = 1
        while i <= n*n:
            for c in range(left, right+1):
                res[top][c] = i
                i += 1
            top+=1
            for r in range(top, bottom + 1):
                res[r][right] = i
                i+=1
            right -= 1
            if top <= bottom:
                for c in range(right, left-1, -1):
                    res[bottom][c] = i
                    i += 1
                bottom -= 1
            
            if left <= right:
                for r in range(bottom, top-1, -1):
                    res[r][left] = i
                    i+=1
                left+=1
        return res
            
        