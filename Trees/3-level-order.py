# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
from collections import deque
from typing import Optional, List
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        queue = deque([root])
        arr = [[root.val]]
        while queue:
            levels = []
            for _ in range(len(queue)): 
                node = queue.popleft()
                if node.left:
                    levels.append(node.left.val)
                    queue.append(node.left)
                if node.right:
                    levels.append(node.right.val)
                    queue.append(node.right)
            if levels:
                arr.append(levels)
        return arr


def main():
    root = TreeNode(2)
    root.left = TreeNode(3)
    root.right = TreeNode(4)
    root.left.left = TreeNode(5)
    root.right.right = TreeNode(6)
    print(Solution().levelOrder(root))

main()