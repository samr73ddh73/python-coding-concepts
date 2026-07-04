# LCA (Lowest Common Ancestor) - Pattern & Time Complexity
#
# PROBLEM: Find the lowest (deepest) node that is ancestor to both p and q
#
# KEY INSIGHT: Post-order DFS
# - Go down to leaves first
# - On the way back up, check if left and right subtrees contain the target nodes
# - LCA is the first node where both p and q are found
#
# PATTERN:
#   1. Base case: If current node is null OR matches p or q → return it
#   2. Recurse left and right
#   3. Check results:
#      - If both left and right found something → current node is LCA
#      - If only one side found something → return that side
#      - If neither found anything → return None
#
# TIME COMPLEXITY: O(n)
#   - Visit each node once in worst case (when LCA is root)
#   - O(h) best case if nodes are close together (h = height)
#
# SPACE COMPLEXITY: O(h)
#   - Recursion call stack depth = tree height

# ============================================
# APPROACH 1: Generic Binary Tree (node references)
# ============================================
# Use when you have TreeNode references for p and q
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # Base: found one of the target nodes OR reached null
        if not root or root == p or root == q:
            return root

        # Recurse both subtrees
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        # Analysis:
        # - Both found: p and q in different subtrees → root is LCA
        # - One found: both p and q in same subtree → return that side
        # - None found: shouldn't happen (p and q exist)
        if left and right:
            return root

        return left or right  # Return whichever side found something


# ============================================
# APPROACH 2: BST (using value comparisons)
# ============================================
# More efficient for BST - use value ordering to prune
class SolutionBST:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # Ensure p.val < q.val
        if p.val > q.val:
            p, q = q, p

        def dfs(node):
            if not node:
                return None

            # Both p and q in left subtree
            if node.val > q.val:
                return dfs(node.left)
            # Both p and q in right subtree
            elif node.val < p.val:
                return dfs(node.right)
            # p and q on different sides OR node is one of them → this is LCA
            else:
                return node

        return dfs(root)


# TIME COMPLEXITY (BST): O(h) where h is height
#   - Prunes entire subtrees based on BST property
#   - O(log n) average case, O(n) worst case (skewed tree)


# ============================================
# APPROACH 3: With Parent Pointers (if available)
# ============================================
# Use when each node has a parent pointer
class SolutionWithParent:
    def lowestCommonAncestor(self, p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # Find path from p to root
        ancestors = set()
        while p:
            ancestors.add(p)
            p = p.parent

        # Walk from q to root until we find a node in p's path
        while q:
            if q in ancestors:
                return q
            q = q.parent

        return None  # Never reached if p and q valid


# ============================================
# TESTING PATTERNS
# ============================================
# Tree:       3
#            / \
#           5   1
#          / \  / \
#         6  2 0  8
#           / \
#          7   4
#
# LCA(5, 1) = 3 (both in different subtrees)
# LCA(5, 2) = 5 (2 is in 5's subtree)
# LCA(6, 2) = 5 (both under 5)
# LCA(2, 4) = 2 (both under 2)


# ============================================
# WHEN TO USE EACH
# ============================================
# Generic DFS:    O(n), works for any tree, simple logic
# BST approach:   O(log n avg), requires BST property, faster
# Parent pointer: O(h), if parent pointers available, alternative approach
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root or root == p or root == q:
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        if left and right:
            return root

        return left or right     