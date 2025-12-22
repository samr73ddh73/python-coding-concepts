# https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/description/

from typing import List
class Solution:
    def findMin(self, nums: List[int]) -> int:
        start, end = 0, len(nums)-1
        minEle = float('inf')
        while(start <= end):
            mid = (start+end)//2
            if nums[start] == nums[mid] == nums[end]:
                minEle =  min(nums[start], minEle)
                start +=1
                end -= 1
            elif nums[mid]<= nums[end] and nums[mid]<= nums[start]: #right is sorted
                minEle = min(nums[mid], minEle)
                end = mid-1
            elif nums[mid] >= nums[start] and nums[mid]>= nums[end]:
                minEle = min(nums[start], minEle)
                start = mid+1
            elif nums[mid] >= nums[start] and nums[mid]<= nums[end]:
                minEle = min(nums[start], minEle)
                return minEle
        return minEle
        
def main():
    ans = Solution().findMin([3,3,1,3])
    print(ans)

main()

