# https://leetcode.com/problems/maximum-difference-between-node-and-ancestor/description/


# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


## For every question, should we compute something from top to bottom (pass it as args) or botton to top (return vals)
class Solution:
    maxVal = float('-inf')
    def maxAncestorDiff(self, root: Optional[TreeNode]) -> int:
        self.maxVal = float('-inf')
        if not root:
            return None
        self.dfs(root,root.val, root.val)
        return self.maxVal

    def dfs(self, root, minI, maxI):
        if not root.left and not root.right:
            self.maxVal = max(self.maxVal, maxI-minI)
            return
        if root.left:
            self.dfs(root.left, min(minI, root.left.val), max(maxI, root.left.val))
        if root.right:
            self.dfs(root.right, min(minI, root.right.val), max(maxI, root.right.val))
        