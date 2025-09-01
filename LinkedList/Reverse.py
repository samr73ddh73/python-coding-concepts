class LinkedList:
    def reverse(head):
        stack = []
        temp = head 
        while(temp):
            stack.append(temp.val)
            temp = temp.next
        temp = head
        while(temp):
            temp.val = stack.pop()
            temp = temp.next
        return head

    def reverse2(head):
        if(head and not head.next):
            return head
        curr, prev = head, None
        while(curr):
            next = curr.next
            curr.next = prev
            prev = curr
            curr = next
        return prev

    def reverse3(prev, curr):
        if(not curr):
            return prev
        next = curr.next
        curr.next = prev
        prev = curr
        curr = next
        return reverse3(prev, curr)
        
        
        