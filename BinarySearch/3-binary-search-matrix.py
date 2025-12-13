# https://leetcode.com/problems/search-a-2d-matrix/description/
from typing import List

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        m, n = len(matrix), len(matrix[0])
        def getCoord(index):
            j = index - (n *(index//n))
            i = index//n
            return i,j
        
        left, right = 0, m*n-1
        while(left <= right):
            mid = (left + right)//2
            i,j = getCoord(mid)
            print(mid, i, j, matrix[i][j])
            if matrix[i][j] == target:
                return True
            elif matrix[i][j] < target:
                left = mid+1
            else:
                right = mid-1

        return False
    #    j = 9 - (4*9/4) = 1
    #    i = 9/4 = 2

    #    4 = n

    #    j = 6 - (4*6/4) = 2
    #    i = 6/4 = 1
