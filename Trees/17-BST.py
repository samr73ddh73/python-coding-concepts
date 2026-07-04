# https://leetcode.com/problems/minimum-absolute-difference-in-bst/
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right



# remember this pattern
class Solution:
    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:
        self.prev = None
        self.minDif = float('inf')
        def inorder(root):
            if not root:
                return
            inorder(root.left)
            if self.prev:
                self.minDif = min(self.minDif, abs(root.val-self.prev))
            self.prev = root.val
            inorder(root.right)
        inorder(root)
        return self.minDif
        
    