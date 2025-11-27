from typing import List
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # [1,2,0, 0, 0]
        zeroIndex = float('inf')
        for i in range(len(nums)):
            if nums[i] == 0:
                zeroIndex = min(zeroIndex, i)
            else:
                if zeroIndex!= float('inf'):
                    nums[zeroIndex] = nums[i]
                    nums[i] = 0
                    zeroIndex += 1
        return nums 
            
        
        