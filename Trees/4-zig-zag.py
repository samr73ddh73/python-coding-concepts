# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

from collections import deque
from typing import Optional
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        left = True
        queue = deque([root])
        ans = []
        levels = []
        while queue:
            print(left, queue)
            levels = []
            for _ in range(len(queue)):
                node = queue.popleft()
                levels.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            if not left:
                levels = levels[::-1]
            left = not left
            ans.append(levels)
        return ans

# We can also pop from left and right since we are using deque