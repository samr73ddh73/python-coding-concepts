# 🎯 LinkedList Tips & Tricks

> Essential tips for linked list problems and patterns

---

## Critical Tips

### Always Think of Edge Cases Around the Head!

- When removing/modifying the head node, handle separately or use **dummy node pattern**
- Dummy node simplifies head removal: `dummy = ListNode(0); dummy.next = head`
- Use dummy when you might need to remove the head itself

### Two-Pointer Pattern for Linked Lists

**Fast-Slow Gap Technique:**
- Use n+1 gap (advance fast by n+1) to land slow **BEFORE** target
- Example: Remove nth from end → fast ahead by n+1, then move both until fast reaches end
- Key: Slow is at node BEFORE the one you want to modify

**Floyd's Cycle Detection:**
- Detect cycle in linked list: slow moves 1 step, fast moves 2 steps
- If they meet, cycle exists; if fast reaches null, no cycle
- Time: O(n), Space: O(1)

### Common Linked List Mistakes

| Mistake | Fix |
|---------|-----|
| Forget to handle head removal | Use dummy node or explicit check |
| Don't update pointers correctly | Always update `prev.next` or node pointers |
| Forget to traverse full list | Check while loop condition carefully |
| Lose reference to head | Use dummy or store in variable first |
| Wrong gap calculation | n+1 gap (not n) to land BEFORE target |

---

## Patterns by Operation

### Removal/Deletion

**Pattern: Dummy Node**
```python
dummy = ListNode(0)
dummy.next = head
prev = dummy
curr = head
# Now safe to handle head removal
```

**When to use:** Any operation that might affect the head

### Cycle Detection

**Floyd's Algorithm:**
```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow == fast:
        return True  # Cycle found
return False  # No cycle
```

**Finding Cycle Start:**
- After detecting cycle, reset one pointer to head
- Move both one step at a time
- They meet at cycle start

---

## Time & Space Complexity

| Operation | Time | Space | Note |
|-----------|------|-------|------|
| Traverse | O(n) | O(1) | Single pass |
| Find element | O(n) | O(1) | Linear search |
| Reverse | O(n) | O(1) | In-place with pointers |
| Cycle detection | O(n) | O(1) | Floyd's algorithm |
| Merge sorted | O(m+n) | O(1) | Two pointers |
| Remove nth | O(n) | O(1) | Two pointer gap technique |

---

## Edge Cases for Linked Lists

- **Empty list** (head = None)
- **Single node** (head.next = None)
- **Two nodes**
- **Remove head** (special case)
- **Cycle in list** (infinite loop risk!)
- **Disconnected lists** (operations on two separate lists)
- **Duplicate values** (handling may matter)

---

## Interview Tips

1. **Always ask:** "Can I use extra space or must it be O(1)?"
2. **Use dummy node:** Simplifies most head-related operations
3. **Draw it out:** Visualize pointer movements
4. **Handle edge cases:** Empty, single node, head removal
5. **Check for cycles:** Risk if modification during traversal
6. **Be careful with pointers:** Easy to lose references

---

*Tips extracted from code and manual review. Keep updating as you discover patterns!*
