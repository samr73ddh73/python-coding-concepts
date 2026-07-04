# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import List
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]):
        if not preorder or not inorder:
            return None
        rootVal = preorder[0]
        mid = inorder.index(rootVal)
        root = TreeNode(rootVal)
        root.left = self.buildTree(preorder[1: mid+1], inorder[:mid])
        root.right = self.buildTree(preorder[mid+1:], inorder[mid+1:])
        return root