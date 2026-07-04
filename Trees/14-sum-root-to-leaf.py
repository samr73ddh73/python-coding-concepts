# Definition for a binary tree node.
# https://leetcode.com/problems/sum-root-to-leaf-numbers/

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
from typing import Optional

class Solution:
    finalSum = 0
    def sumNumbers(self, root: Optional[TreeNode]) -> int:
        self.dfs(root, root.val)
        return self.finalSum
    def dfs(self, root, number):
        if not root.left and not root.right:
            self.finalSum += number
            return
        if root.left:
            self.dfs(root.left, number*10 + root.left.val)
        if root.right:
            self.dfs(root.right, number*10 + root.right.val)
        return
