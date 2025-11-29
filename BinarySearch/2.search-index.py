class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        upperBound = len(nums)
        x = target
        left, right = 0, len(nums)-1
        while(left <= right):
            mid = (left + right)//2
            print(left, right, mid)
            if nums[mid] == x:
                return mid
            elif nums[mid] > x:
                right = mid-1 
                upperBound = mid
            else:
                left = mid+1
        return upperBound      
