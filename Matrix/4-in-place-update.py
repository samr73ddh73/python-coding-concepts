class Solution(object):
    def gameOfLife(self, board):
        if not board or not board[0]:
            return

        m, n = len(board), len(board[0])

        def count_live_neighbors(r, c):  # add this in notes, whenever we need to move in directions in a matrix
            count = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and abs(board[nr][nc]) == 1:
                        count += 1
            return count

        for r in range(m):
            for c in range(n):
                live_neighbors = count_live_neighbors(r, c)

                if board[r][c] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                    board[r][c] = -1
                elif board[r][c] == 0 and live_neighbors == 3:
                    board[r][c] = 2

        for r in range(m):
            for c in range(n):
                if board[r][c] > 0:
                    board[r][c] = 1
                else:
                    board[r][c] = 0