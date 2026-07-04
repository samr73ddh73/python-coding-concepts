# Definition for a binary tree node.
from typing import List, Optional
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# The pattern here is:
# 1. Find root from preorder, then find a way to get the partition, we can do it from sorted array as we do it from inorder
class Solution:
    def bstFromPreorder(self, preorder: List[int]) -> Optional[TreeNode]:
       bstarr = sorted(preorder)
       return self.construct(preorder, bstarr)

    def construct(self, preorder, bstarr):
        if not preorder or not bstarr:
            return None
        rootVal = preorder[0]
        root = TreeNode(rootVal)
        mid = bstarr.index(rootVal)
        root.left = self.construct(preorder[1:mid+1], bstarr[:mid])
        root.right = self.construct(preorder[mid+1:], bstarr[mid+1:])
        return root
