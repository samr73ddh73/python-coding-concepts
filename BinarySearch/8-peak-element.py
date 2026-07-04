# https://leetcode.com/problems/find-peak-element/description/

#Concept: go whereever the slope is increasing.
from typing import List
class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        l, r = 0, len(nums)-1
        if len(nums) == 1:
            return 0
        
        while(l<=r):
            mid = (l+r)//2
            if mid == 0:
                if nums[mid] > nums[mid+1]:
                    return mid
                else:
                    l = mid + 1
                    continue
            if mid == len(nums)-1:
                if nums[mid] < nums[mid-1]:
                    return mid
                else:
                    r = mid-1
                    continue
            if nums[mid] > nums[mid-1] and nums[mid] > nums[mid+1]:
                return mid
            if nums[mid] < nums[mid+1]:
                l = mid+1
            else:
                r = mid -1
        return mid
