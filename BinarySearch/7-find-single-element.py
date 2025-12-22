#https://leetcode.com/problems/single-element-in-a-sorted-array/

from typing import List
class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        start, end = 0, len(nums)-1
        while(start<= end):
            mid =(start + end)//2
            if mid%2 == 0:
                if mid+1 == len(nums):
                    return nums[mid]
                if (mid+1) < len(nums) and nums[mid+1]!= nums[mid]:
                    if nums[mid-1]!= nums[mid]:
                        return nums[mid]
                    else:
                        end = mid-1
                elif (mid+1) < len(nums) and nums[mid+1]== nums[mid]:
                    start = mid + 1
            else:
                if mid>0 and nums[mid-1] != nums[mid]:
                    end = mid-1
                else:
                    start = mid + 1
        return -1
            
            
def main():
    ans = Solution().singleNonDuplicate([1,1,2,3,3,4,4])
    print(ans)

main()