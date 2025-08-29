class ListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init(self):
        self.head = None
    def insertAtEnd(data):
        node = ListNode(data)
        if(not self.head):
            self.head = node
            return
        curr = self.head
        while(curr.next):
            curr = curr.next
        curr.next = node
    def insertAtBeg(data):
        node = ListNode(data)
        curr = self.head
        self.head = node
        node.next = curr

class DListNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
class DLL:
    def __init(self):
        self.head = None
    def insertAtEnd(data):
        node = ListNode(data)
        if(not self.head):
            self.head = node
            return
        curr = self.head
        while(curr.next):
            curr = curr.next
        curr.next = node
    def insertAtBeg(data):
        node = ListNode(data)
        curr = self.head
        self.head = node
        node.next = curr

