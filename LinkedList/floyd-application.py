#Beautiful Question
# https://leetcode.com/problems/find-the-duplicate-number/
from types import List
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        slow, fast = 0, 0
        while(True):
            slow = nums[slow]
            fast = nums[nums[fast]]
            print(slow, fast)
            if slow == fast:
                break
        print("out", slow, fast)
        slow, i = 0,0
        while(slow!=fast):
            slow = nums[slow]
            fast = nums[fast]
            
            print("same", slow, fast)
        return slow