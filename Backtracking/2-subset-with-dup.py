from typing import List

class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []
        self.helper(0, nums, [], result)
        return result

    def helper(self, i, nums, curr, output):
        output.append(curr[:])
        for j in range(i, len(nums)):
            if j > i and nums[j] == nums[j-1]:
                continue
            curr.append(nums[j])
            self.helper(j+1, nums, curr, output)
            curr.pop()
    