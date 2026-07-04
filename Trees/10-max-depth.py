# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
from typing import Optional
class Solution:
    maxLevel = -1
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        self.dfs(root, 1)
        return self.maxLevel
        
    def dfs(self, root, level):
        if not root:
            return
        self.maxLevel = max(level, self.maxLevel)
        self.dfs(root.left, level+1)
        self.dfs(root.right, level+1)



# Cleanest Approach
def maxDepth(self, root):
    if not root:
        return 0
    return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))