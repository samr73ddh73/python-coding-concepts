# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
from typing import Optional
class Solution:
    finalPath = []
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        self.finalPath = []
        if not root:
            return []
        self.dfs(root, [root.val], root.val, targetSum)
        return self.finalPath
    
    def dfs(self, root, path, sum, targetSum):
        print(root.val, sum, targetSum)
        if not root.left and not root.right and sum == targetSum:
            print("I'm in", path, root.val, sum, targetSum)
            self.finalPath.append(path[:])
            return
        if root.left:
            path.append(root.left.val)
            self.dfs(root.left, path, sum+root.left.val, targetSum )
            left = path.pop()
            # sum = sum-left
        if root.right:
            path.append(root.right.val)
            self.dfs(root.right, path, sum+root.right.val, targetSum )
            right = path.pop()
            # sum = sum-right
        return 
        
        