def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        dia = 0
        def height(root):
            if not root:
                return 0
            leftH = height(root.left)
            rightH = height(root.right)
            nonlocal dia
            dia = max(dia, leftH+rightH)
            return 1 + max(leftH, rightH)
        height(root)
        return dia