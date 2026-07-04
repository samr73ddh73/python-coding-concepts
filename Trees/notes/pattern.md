1. Level order is easy, always use BFS (queue)
2. Whenever a tree question needs traversal up to it's parent as well, we can simply add parent map and then do normal graph like bfs. (que: https://leetcode.com/problems/all-nodes-distance-k-in-binary-tree/description/)
3. Tree construction problems:
#### The Core Insight

> **Preorder gives you the root. Inorder tells you what's on the left vs right of that root.**

```
preorder = [3, 9, 20, 15, 7]
inorder  = [9, 3, 15, 20, 7]
```

- `preorder[0] = 3` → **3 is the root**
- Find 3 in inorder → index 1
- Everything **left of 3** in inorder = `[9]` → left subtree
- Everything **right of 3** in inorder = `[15, 20, 7]` → right subtree
- Left subtree has **1 node**, so in preorder, next 1 element = `[9]` = left subtree's preorder
- Remaining `[20, 15, 7]` = right subtree's preorder

Then **recurse** on each half. That's the entire algorithm.

---

## The Pattern — Always These 3 Steps

```
1. Use one traversal to identify the ROOT
2. Use the other traversal to SPLIT left/right subtrees  
3. Recurse on each half with the corresponding slices
```

| Given | Root from | Split using |
|---|---|---|
| Preorder + Inorder | `preorder[0]` | inorder index of root |
| Postorder + Inorder | `postorder[-1]` | inorder index of root |
| Preorder + Postorder | `preorder[0]` | `preorder[1]` is left root, find in postorder |

**Why inorder is always needed?** Because pre/post order alone can't tell you the boundary between left and right subtrees. Inorder is the "splitter".

---

## The Code

```python
def buildTree(preorder, inorder):
    if not preorder or not inorder:
        return None

    root_val = preorder[0]                    # Step 1: root
    root = TreeNode(root_val)

    mid = inorder.index(root_val)             # Step 2: split point

    # Step 3: recurse
    # left subtree has `mid` nodes — use that to slice preorder too
    root.left  = buildTree(preorder[1 : 1+mid], inorder[:mid])
    root.right = buildTree(preorder[1+mid:],    inorder[mid+1:])

    return root
```

The **size of left subtree = `mid`** is the key — it lets you slice preorder correctly even though preorder doesn't directly show the split.

![alt text](image.png)




- Another imp pattern for recursion and dfs is how to compute the results botton up in an optimal way using sentinal values.

````md
# Sentinel Value Pattern in Recursion

## Core Idea

A recursive function can return:

- a **valid value**
- OR a **special sentinel value** indicating failure

This helps combine:
1. computation
2. validation/error propagation

into a single DFS.

---

# Example: Balanced Binary Tree

Normally:
- return subtree height

Special case:
- return `-1` if subtree is unbalanced

```python
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
````

---

# Why This Works

Each subtree reports information upward:

* valid height
* OR failure

Parent immediately propagates failure upward.

This avoids recomputation and makes solution `O(n)`.

---

# General Pattern

```python
def dfs(node):
    if failure_condition:
        return SENTINEL

    left = dfs(node.left)
    if left == SENTINEL:
        return SENTINEL

    right = dfs(node.right)
    if right == SENTINEL:
        return SENTINEL

    if current_invalid:
        return SENTINEL

    return valid_answer
```

---

# Mental Model

Instead of thinking:

> "How do I traverse the tree?"

Think:

> "What should each node RETURN to its parent?"

This is the key to mastering recursive tree problems.

---

# Common Sentinel Values

| Meaning    | Sentinel       |
| ---------- | -------------- |
| invalid    | `-1`           |
| impossible | `float('inf')` |
| not found  | `None`         |
| failure    | `False`        |

Sentinel should be:

* impossible as a valid answer
* easy to check

---

# Where This Pattern Appears

* Balanced Binary Tree
* Validate BST
* Diameter of Tree
* Maximum Path Sum
* Graph DFS
* DP impossible states
* Expression parsing

---

# Important Related Concept

## Bottom-Up DFS (Postorder)

Children solve themselves first.

Parent combines their answers.

This is one of the most important tree recursion patterns.

```
```


# Remember: Min Depth, Shortest Path => USE BFS