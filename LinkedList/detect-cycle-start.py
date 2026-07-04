# Intuition: https://www.youtube.com/watch?v=2Kd0KKmmHFc&t=8s

class ListNode:
    def __init__(self, val):
        self.val = val
        self.next = None

def detectCycle(head: ListNode):
    slow, fast = head, head
    while( fast and fast.next):
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

def getCycleStart(head: ListNode):
    slow, fast = head, head
    while( fast and fast.next):
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            break
    if not fast:
        return None
    slow = head
    while(slow!= fast):
        slow = slow.next 
        fast = fast.next 
    return fast.val     

def main():
    head = ListNode(1)
    head.next = ListNode(2)
    head.next.next = ListNode(3)
    temp = head.next.next
    temp.next = ListNode(4)
    temp.next.next = temp
    startPoint = getCycleStart(head)
    print(startPoint)

main()