#check the sentinal pattern approach in patterns

# Sentinel Value Pattern in Recursion

## Core Idea

# A recursive function can return:

# - a **valid value**
# - OR a **special sentinel value** indicating failure

# This helps combine:
# 1. computation
# 2. validation/error propagation

# into a single DFS.

# ---

# # Example: Balanced Binary Tree

# Normally:
# - return subtree height

# Special case:
# - return `-1` if subtree is unbalanced


def dfs(node):
    if not node:
        return 0

    left = dfs(node.left)
    if left == -1:
        return -1

    right = dfs(node.right)
    if right == -1:
        return -1

    if abs(left - right) > 1:
        return -1

    return 1 + max(left, right)

def isBalanced(root):
    return dfs(root) != -1