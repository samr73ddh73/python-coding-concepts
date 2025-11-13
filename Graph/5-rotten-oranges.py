def orangesRotting(self, grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return -1

    rows, cols = len(grid), len(grid[0])
    queue = deque()
    visited = set()
    fresh_count = 0

    # Initialize
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c, 0))  # (row, col, time)
                visited.add((r, c))
            elif grid[r][c] == 1:
                fresh_count += 1

    if fresh_count == 0:
        return 0

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    max_minutes = 0  # Track maximum time

    while queue:
        row, col, minutes = queue.popleft()
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if (0 <= new_row < rows and
                0 <= new_col < cols and
                (new_row, new_col) not in visited and
                grid[new_row][new_col] == 1):

                visited.add((new_row, new_col))
                fresh_count -= 1
                # The NEW orange rots at (minutes + 1)
                new_time = minutes + 1
                max_minutes = max(max_minutes, new_time)  # ✅ Update max
                queue.append((new_row, new_col, new_time))

    # Return max_minutes if all oranges rotted, else -1
    return max_minutes if fresh_count == 0 else -1


# Time	Space	Correctness
# Level-by-level	O(m×n)	O(m×n)	✅ Guaranteed correct