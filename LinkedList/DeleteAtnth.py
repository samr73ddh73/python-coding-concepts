# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

# For ll, always think of edge cases around the head!!
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        size = 0
        temp = head
        while(temp):
            temp = temp.next
            size = size + 1
        index, i  = size - n + 1, 1
        prev = None
        temp = head
        print("size", size, index)
        while(temp):
            if(i==index):
                if(prev):
                    prev.next = temp.next
                    return head
                head = head.next
                return head
            prev = temp
            temp = temp.next
            i = i+1
        return head


Better two pointer solution:

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        res = ListNode(0, head)
        dummy = res

        for _ in range(n):
            head = head.next
        
        while head:
            head = head.next
            dummy = dummy.next
        
        dummy.next = dummy.next.next

        return res.next

