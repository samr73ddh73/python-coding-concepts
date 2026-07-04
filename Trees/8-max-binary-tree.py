# https://leetcode.com/problems/maximum-binary-tree/description/

# Definition for a binary tree node.
from typing import List, Optional
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def constructMaximumBinaryTree(self, nums: List[int]) -> Optional[TreeNode]:
        return self.constructMax(nums)
    def constructMax(self, nums):
        if not nums:
            return None
        rootVal= max(nums)
        mid = nums.index(rootVal)
        root = TreeNode(rootVal)
        root.left = self.constructMax(nums[:mid])
        root.right = self.constructMax(nums[mid+1:])
        return root
