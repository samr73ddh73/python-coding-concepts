from collections import deque

class Solution:
    def findMinMove(n, board):
        n = len(board)
        right = True
        indx = 1
        grid = [-1 for _ in range(n*n + 1)]
        for i in range(n-1, -1, -1):
            if right:
                for j in range(0, n):
                    grid[indx] = board[i][j]
                    indx +=1
            else:
                for j in range(n-1,-1,-1):
                    grid[indx] = board[i][j]
                    indx +=1
            right = not right
        visited = set()  # O(1) lookup, O(V) space
        queue = deque([1])
        move = 0
        while(queue):
            size = len(queue)
            while(size > 0):
                cell = queue.popleft()
                if cell == n*n:
                    return move
                for i in range(1, 7):
                    next = cell + i
                    if next <= n*n:
                        if grid[next]!= -1:
                            next = grid[next]
                        if next not in visited:
                            queue.append(next)
                            visited.add(next)
                size -= 1
            move += 1
        return -1
                    
