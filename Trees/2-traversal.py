class TreeNode:
    def __init__(self, val = 0, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

def inorder(root: TreeNode, res = []):
    if root is not None:
        inorder(root.left, res)
        res.append(root.val)
        inorder(root.right, res)
    return res

def inorder_nonrecursive(root: TreeNode):
    res = []
    stack = []
    while(1):
        while(root):
            stack.append(root)
            root = root.left
        if len(stack) == 0:
            break
        res.append(stack.pop().val)
        root = root.right
    return res


def preorder(root: TreeNode, res = []):
    if root is not None:
        res.append(root.val)
        preorder(root.left)
        preorder(root.right)
    return res

def preorder_nonrecursive(root: TreeNode):
    res = []
    stack = []
    while(1):
        while(root):
            res.append(root.val)
            stack.append(root)
            root = root.left
        if len(stack) == 0:
            break
        root = stack.pop()
        root = root.right

def postorder(root: TreeNode, res = []):
    if root is not None:
        
        postorder(root.left)
        postorder(root.right)
        res.append(root.val)
    return res

def postorder_nonrecursive(root: TreeNode):
    res = []
    stack = []
    while(1):
        while(root):
            stack.append(root)
            root = root.left
        if len(stack) == 0:
            break
        while(not root.left and not root.right):
            res.append(stack.pop().val)
        root = stack[-1]
        if(not root.left and not root.right):
            res.append(stack.pop().val)
        root = root.right