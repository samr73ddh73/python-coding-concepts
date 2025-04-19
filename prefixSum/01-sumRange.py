https://leetcode.com/problems/range-sum-query-immutable/?envType=problem-list-v2&envId=prefix-sum
class NumArray:

    def __init__(self, nums: List[int]):
        self.prefix_sum = [0]
        self.nums = nums
        i = 0
        for num in nums:
            self.prefix_sum.append(self.prefix_sum[i]+num)
            i = i +1

    def sumRange(self, left: int, right: int) -> int:
        if left < len(self.prefix_sum) and right<len(self.prefix_sum):
            return self.prefix_sum[right]-self.prefix_sum[left] + self.nums[right]


        


# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(left,right)