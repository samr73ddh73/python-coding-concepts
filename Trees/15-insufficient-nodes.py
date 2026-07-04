# https://leetcode.com/problems/insufficient-nodes-in-root-to-leaf-paths/description/

# Definition for a binary tree node.



# TRICK: Removing nodes from tree
#
# ❌ WRONG: Reassigning the local variable
#     if sum < limit:
#         root = None  # Only changes local variable, parent still has old reference!
#     return False
#
# ✓ CORRECT: Return None and let parent update its reference
#     if sum < limit:
#         return None  # Parent receives this and does: root.left = dfs(...)
#
# Why? Objects pass by reference, but reassigning the variable (root = None)
# only breaks the LOCAL reference. The parent's child pointer is unchanged.
# The parent must capture the return value: root.left = self.dfs(root.left, ...)
# This way, if dfs returns None, the parent updates its own pointer to None.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import Optional

class Solution:
    def sufficientSubset(self, root: Optional[TreeNode], limit: int) -> Optional[TreeNode]:
        if not root:
            return root
        root = self.dfs(root, root.val, limit)
        return root
    def dfs(self, root, sum, limit):
        if not root.left and not root.right:
            if sum < limit:
                print("makingit null", root.val)
                return None
            return root
        left, right = None, None
        if root.left:
           left = self.dfs(root.left, sum + root.left.val, limit)
           root.left = left
        if root.right:
            right = self.dfs(root.right, sum + root.right.val, limit)
            root.right = right
        if not left and not right:
            return None
        return root