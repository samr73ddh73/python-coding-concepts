from typing import List
from recviz import recviz
class Solution:
    @recviz
    def subsets(self, nums: List[int]) -> List[List[int]]:
        output = [] 
        self.helper(0, [], nums, output)
        return output

    def helper(self, i, curr, nums, output):
        output.append(curr[:])
        for j in range(i, len(nums)):
            curr.append(nums[j])
            self.helper(j+1, curr, nums, output)
            curr.pop()
        
def main():
    nums = [1,2,3,4]
    Solution().subsets(nums)

main()