# Tree Patterns Cheatsheet — Quick Revision

## 1. TRAVERSAL CHOICE: DFS vs BFS

| Use Case | Method | Why |
|----------|--------|-----|
| **Path problems** (root to leaf) | DFS (PreOrder) | Track path as you go down |
| **Sum/Product along paths** | DFS (PreOrder) | Accumulate values while traversing |
| **Level-wise problems** | BFS (Queue) | Need horizontal information (width, level nums) |
| **Deepest/Shallowest nodes** | BFS or DFS | Both work, BFS is clearer for "first level" |
| **Ancestor/LCA problems** | DFS (PostOrder) | Need info from children first |
| **Construction from traversals** | DFS | Build subtrees recursively |

---

## 2. IN-ORDER TRAVERSAL TRICKS

### Access Previous Node (In-order)
**Pattern:** Track `prev` node during in-order traversal (Left → Node → Right)

```python
# For finding pairs, differences, validation
prev = None

def inorder(node):
    global prev
    if not node:
        return
    
    inorder(node.left)
    
    # Process current node with prev
    if prev:
        # Do something with prev and node
        pass
    prev = node
    
    inorder(node.right)
```

**Use cases:**
- Validate BST (check prev.val < node.val)
- Find k-th smallest (count nodes in order)
- Minimum absolute difference in BST

### Iterative In-order (Stack-based)
```python
def inorder_iterative(root):
    stack, curr = [], root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        # Process curr
        prev = curr  # Track previous
        curr = curr.right
```

---

## 3. DFS FOR PATH PROBLEMS

### Root to Leaf Path Pattern
```python
def dfs(node, current_path, result):
    # Base: leaf node
    if not node.left and not node.right:
        result.append(current_path)  # or list(current_path)
        return
    
    # Explore left
    if node.left:
        current_path.append(node.left.val)
        dfs(node.left, current_path, result)
        current_path.pop()  # Backtrack (if using list)
    
    # Explore right
    if node.right:
        current_path.append(node.right.val)
        dfs(node.right, current_path, result)
        current_path.pop()  # Backtrack
```

**Key tricks:**
- Use list + backtrack (pop) for mutable structures
- Use string concatenation for immutable approach
- Always copy before storing: `result.append(list(current_path))`

### Sum Along Paths
```python
def dfs(node, current_sum):
    if not node.left and not node.right:
        return current_sum
    
    left_sum = dfs(node.left, current_sum + node.left.val) if node.left else 0
    right_sum = dfs(node.right, current_sum + node.right.val) if node.right else 0
    
    return left_sum + right_sum
```

---

## 4. LCA (LOWEST COMMON ANCESTOR)

### Generic Binary Tree (Post-order DFS)
```python
def lca(root, p, q):
    if not root or root == p or root == q:
        return root
    
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    
    # Both found in different subtrees → current is LCA
    if left and right:
        return root
    # One side has both → return that side
    return left or right
```

**Time:** O(n) | **Space:** O(h)

### BST Optimization (Prune with values)
```python
def lca_bst(root, p, q):
    if p.val > q.val:
        p, q = q, p
    
    def dfs(node):
        if not node:
            return None
        
        if node.val > q.val:           # Both on left
            return dfs(node.left)
        elif node.val < p.val:         # Both on right
            return dfs(node.right)
        else:                          # Spanning → this is LCA
            return node
    
    return dfs(root)
```

**Time:** O(log n avg) | **Better than generic when it's a BST**

### LCA of Deepest Leaves
```python
def lca_deepest(root):
    def dfs(node):
        if not node:
            return (0, None)  # (height, lca_node)
        
        left_h, left_lca = dfs(node.left)
        right_h, right_lca = dfs(node.right)
        
        # Same height → deepest leaves on both sides
        if left_h == right_h:
            return (left_h + 1, node)
        # Left deeper
        elif left_h > right_h:
            return (left_h + 1, left_lca)
        # Right deeper
        else:
            return (right_h + 1, right_lca)
    
    h, lca = dfs(root)
    return lca
```

---

## 5. HEIGHT/DEPTH PROBLEMS

### Get Height of Node
```python
# Height = distance to farthest leaf
def height(node):
    if not node:
        return 0
    return 1 + max(height(node.left), height(node.right))
```

### Check Balanced Tree
```python
def is_balanced(node):
    if not node:
        return True
    
    left_h = height(node.left)
    right_h = height(node.right)
    
    # Difference at most 1 AND both subtrees balanced
    return (abs(left_h - right_h) <= 1 and 
            is_balanced(node.left) and 
            is_balanced(node.right))
```

**Optimization:** Return (bool, height) tuple to avoid recalculating heights

```python
def is_balanced_opt(node):
    def helper(node):
        if not node:
            return (True, 0)
        
        left_balanced, left_h = helper(node.left)
        right_balanced, right_h = helper(node.right)
        
        is_bal = (left_balanced and right_balanced and 
                  abs(left_h - right_h) <= 1)
        return (is_bal, 1 + max(left_h, right_h))
    
    return helper(node)[0]
```

### Diameter (Longest Path)
```python
def diameter(root):
    max_d = 0
    
    def height(node):
        nonlocal max_d
        if not node:
            return 0
        
        left = height(node.left)
        right = height(node.right)
        max_d = max(max_d, left + right)  # Path through this node
        
        return 1 + max(left, right)
    
    height(root)
    return max_d
```

---

## 6. LEVEL ORDER (BFS) WHEN TO USE

```python
from collections import deque

def level_order_template(root):
    if not root:
        return []
    
    queue = deque([root])
    result = []
    
    while queue:
        level = []
        for _ in range(len(queue)):  # Process one level at a time
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result
```

**Use BFS for:**
- Level-order traversal
- Width of tree (max level size)
- Zigzag patterns
- Even/Odd level separation
- Distance from root (automatically: level = distance)

---

## 7. TREE CONSTRUCTION

### From Preorder + Inorder
```python
def build_tree(preorder, inorder):
    if not preorder:
        return None
    
    # Preorder: root is always first
    root_val = preorder[0]
    root = TreeNode(root_val)
    
    # Find root in inorder: left is everything before, right is after
    root_idx = inorder.index(root_val)
    
    root.left = build_tree(preorder[1:root_idx+1], inorder[:root_idx])
    root.right = build_tree(preorder[root_idx+1:], inorder[root_idx+1:])
    
    return root
```

**Key:** Preorder gives root, Inorder gives left/right split

### From Postorder + Inorder
```python
def build_tree(postorder, inorder):
    if not postorder:
        return None
    
    # Postorder: root is always last
    root_val = postorder[-1]
    root = TreeNode(root_val)
    
    root_idx = inorder.index(root_val)
    
    root.left = build_tree(postorder[:root_idx], inorder[:root_idx])
    root.right = build_tree(postorder[root_idx:-1], inorder[root_idx+1:])
    
    return root
```

**Key:** Postorder gives root, Inorder gives left/right split

---

## 8. QUICK TIPS & TRICKS

| Problem | Trick |
|---------|-------|
| **Next node in BST** | In-order traversal, track prev |
| **Count nodes in subtree** | Return count in DFS |
| **Validate BST** | In-order should be sorted |
| **Max path sum** | DFS return max ending at node, track global max |
| **Serialize/Deserialize** | Use marker nodes for null (e.g., "#") |
| **Lowest to Highest** | Use stack instead of recursion for iterative DFS |
| **Path sum to target** | Use (current_sum, target) — return count or boolean |
| **Find all paths** | Always backtrack with lists |

---

## 9. PROBLEM APPROACH: TOP-DOWN vs BOTTOM-UP

### Decision Framework

```
Does the answer depend on:
├─ Information about CURRENT node + path from root?
│  └─ TOP-DOWN (Pre-order) ✓
│     • Path sum, tracking values from root
│     • Level-based decisions
│     • Example: "paths from root", "sum to target"
│
├─ Information from CHILDREN first?
│  └─ BOTTOM-UP (Post-order) ✓
│     • Heights, counts, validation
│     • LCA, comparing subtrees
│     • Example: "balanced tree", "diameter", "LCA"
│
└─ Level-wise horizontal info?
   └─ BFS (Queue) ✓
      • Width, level ordering
      • "First occurrence at level"
      • Example: "level order", "zigzag"
```

### TOP-DOWN Example: Path Sum
```python
# Question: Find all paths from root with sum == target_sum
def dfs(node, current_sum, target, path):
    if not node:
        return
    
    current_sum += node.val
    path.append(node.val)
    
    # Process at current node (using info from root down to here)
    if not node.left and not node.right and current_sum == target:
        result.append(list(path))
    
    dfs(node.left, current_sum, target, path)
    dfs(node.right, current_sum, target, path)
    
    path.pop()  # Backtrack
```
**Key:** Accumulate info as you go DOWN

### BOTTOM-UP Example: Height
```python
# Question: Get height of each node
def height(node):
    if not node:
        return 0
    
    # FIRST, get info from children
    left_h = height(node.left)
    right_h = height(node.right)
    
    # THEN, compute current node's answer using children's info
    return 1 + max(left_h, right_h)
```
**Key:** Get answers from CHILDREN first, then use them

### Mix: Top-Down Info + Bottom-Up Aggregation
```python
# Question: Max path sum in tree (any node to any node)
def dfs(node):
    if not node:
        return float('-inf'), float('-inf')  # (max_through_node, max_in_subtree)
    
    # Bottom-up: get info from children
    left_through, left_max = dfs(node.left)
    right_through, right_max = dfs(node.right)
    
    # Current node's max path going through it
    max_through_current = node.val + max(0, max(left_through, right_through))
    
    # Best answer in entire subtree
    max_in_subtree = max(max_through_current, left_max, right_max)
    
    return max_through_current, max_in_subtree
```

---

## 10. BACKTRACKING TECHNIQUES

### For Lists: Add-Explore-Remove

**Pattern:**
```python
def backtrack(node, state: list, result):
    # Base case
    if condition:
        result.append(state[:])  # Copy required!
        return
    
    # Add to state
    state.append(something)
    
    # Explore
    backtrack(next, state, result)
    
    # REMOVE to undo changes (critical for mutable lists)
    state.pop()
```

**Example: All Root-to-Leaf Paths**
```python
def paths(node, current_path, result):
    if not node.left and not node.right:
        result.append(current_path[:])  # Copy!
        return
    
    if node.left:
        current_path.append(node.left.val)     # Add
        paths(node.left, current_path, result) # Explore
        current_path.pop()                     # Remove
    
    if node.right:
        current_path.append(node.right.val)    # Add
        paths(node.right, current_path, result)# Explore
        current_path.pop()                     # Remove
```

**Common Mistakes:**
```python
# ❌ WRONG: Forget to pop()
state.append(x)
dfs(left)
state.append(y)  # x is still there!
dfs(right)

# ✓ CORRECT: Always pop() after exploring
state.append(x)
dfs(left)
state.pop()      # Undo x
state.append(y)
dfs(right)
state.pop()      # Undo y
```

### For Numbers: Undo Change

**Pattern:**
```python
def backtrack(node, current_sum, target):
    if not node:
        return count
    
    # Add to running value
    current_sum += node.val
    
    # Process (check condition with modified value)
    if condition(current_sum):
        count += 1
    
    # Explore both branches
    count += backtrack(node.left, current_sum, target)
    count += backtrack(node.right, current_sum, target)
    
    # No need to "remove" because current_sum is local!
    # It automatically reverts when returning
    
    return count
```

**Example: Count paths with sum == target**
```python
def count_paths(node, target, current_sum):
    if not node:
        return 0
    
    current_sum += node.val
    count = 0
    
    # Check if current path sums to target
    if current_sum == target:
        count += 1
    
    # Try both subtrees (current_sum is passed, not modified in place)
    count += count_paths(node.left, target, current_sum)
    count += count_paths(node.right, target, current_sum)
    
    return count
```

**Why no "undo" for numbers?**
- Numbers are primitives (immutable)
- When you return from recursion, the caller's `current_sum` is unchanged
- Each branch gets independent tracking

### Comparison: Lists vs Numbers

| Type | Storage | Backtrack? | Why |
|------|---------|-----------|-----|
| **List** | `state.append(x)` | **YES** `state.pop()` | Mutable — all branches see same list |
| **Number** | `sum + x` | **NO** | Immutable — each branch has own value |
| **String** | `path + str(x)` | **NO** | Immutable — new string each time |

---

## 11. DECISION CHECKLIST

Before coding, ask:

```
1. Do I need to remember the CURRENT PATH?
   └─ YES → Use List + Backtrack (pop) OR String (no pop)
   └─ NO  → Just track numbers/flags

2. Can I solve with information from ROOT down?
   └─ YES → TOP-DOWN (Pre-order), pass info down
   └─ NO  → Need info from CHILDREN → BOTTOM-UP (Post-order)

3. Do I modify a mutable data structure?
   └─ YES → Must backtrack (add-explore-remove)
   └─ NO  → No backtracking needed (primitives)

4. Is order of nodes important?
   └─ Level-wise? → BFS (Queue)
   └─ Root→Leaf?  → DFS (any order)
   └─ Left→Right? → In-order/Level-order
```

---

## 9. TIME COMPLEXITY SUMMARY

| Operation | Worst | Average | BST Best |
|-----------|-------|---------|----------|
| DFS traversal | O(n) | O(n) | O(n) |
| BFS traversal | O(n) | O(n) | O(n) |
| Height | O(n) | O(n) | O(log n) |
| Search | O(n) | O(n) | O(log n) |
| LCA | O(n) | O(n) | O(log n) |
| Construction | O(n) | O(n) | O(n) |
