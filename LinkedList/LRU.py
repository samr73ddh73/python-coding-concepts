class Node:
    def __init__(self, key, val, prev = None, next = None):
        self.val, self.key = val, key
        self.prev, self.next = prev, next

class LRUCache:

    def __init__(self, capacity: int):
        self.cache = {}
        self.capacity = capacity
        self.head = Node(0,0)
        self.tail = Node(0,0)

    def insertAtHead(self, key, val):
        node = Node(key, val)
        prevNode = self.head.next
        if not prevNode:
            self.tail.prev = node
        node.next = prevNode
        self.head.next = node
        if prevNode:
            prevNode.prev = node
        node.prev = self.head
        return node

    def deleteNode(self, node):
        if not node:
            return
        prev = node.prev
        next = node.next
        if prev:
            prev.next = next
        if next:
            next.prev = prev
        if not next:
            self.tail.prev = prev

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self.deleteNode(node)
            node = self.insertAtHead(key, node.val)
            self.cache[key] = node
            return node.val
        return -1


    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            self.deleteNode(node)
        node = self.insertAtHead(key, value)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            lastNode = self.tail.prev
            if not lastNode:
                return
            self.deleteNode(lastNode)
            del self.cache[lastNode.key]






def main():
    """Test LRU Cache with various inputs"""

    print("\n=== Test 1: Basic Operations ===")
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    print(f"get(1) = {lru.get(1)}")  # 1
    lru.put(3, 3)
    print(f"get(2) = {lru.get(2)}")  # -1 (evicted)

    print("\n=== Test 2: Update and Access Order ===")
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    print(f"get(1) = {lru.get(1)}")  # 1 (makes 1 recent)
    lru.put(3, 3)  # evicts 2, not 1
    print(f"get(2) = {lru.get(2)}")  # -1

    print("\n=== Test 3: Update Value ===")
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    lru.put(1, 10)  # update 1
    print(f"get(1) = {lru.get(1)}")  # 10

    print("\n=== Test 4: Capacity 1 ===")
    lru = LRUCache(1)
    lru.put(1, 1)
    lru.put(2, 2)  # evicts 1
    print(f"get(1) = {lru.get(1)}")  # -1
    print(f"get(2) = {lru.get(2)}")  # 2

    print("\n=== Test 5: Complex Sequence (Capacity 3) ===")
    lru = LRUCache(3)
    lru.put(1, 1)
    lru.put(2, 2)
    lru.put(3, 3)
    print(f"get(1) = {lru.get(1)}")  # 1
    lru.put(4, 4)  # evicts 2 (LRU)
    print(f"get(2) = {lru.get(2)}")  # -1
    print(f"get(3) = {lru.get(3)}")  # 3
    print(f"get(4) = {lru.get(4)}")  # 4

    print("\n=== Test 6: Consecutive Operations ===")
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    lru.get(1)
    lru.get(2)
    lru.put(3, 3)  # evicts 1
    print(f"get(1) = {lru.get(1)}")  # -1
    print(f"get(2) = {lru.get(2)}")  # 2
    print(f"get(3) = {lru.get(3)}")  # 3


if __name__ == "__main__":
    main()