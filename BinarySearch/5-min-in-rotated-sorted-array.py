from typing import List
class Solution:
    def findMin(self, nums: List[int]) -> int:
        pivot = self.pivot(nums)
        minIndx = (pivot+1)%len(nums) 
        return nums[minIndx]

    def pivot(self, nums):
        target = nums[0]
        l, r = 0, len(nums)-1
        while(l <= r):
            mid = (l+r)//2
            if nums[mid] >= target:
                pivot = mid
                l = mid+1
            else:
                r = mid-1
        return pivot
        
def main():
    ans = Solution().findMin([ 4, 5,6, 7,8,9, 4, 4, 4, 4, 4, 4])
    print(ans)

main()

