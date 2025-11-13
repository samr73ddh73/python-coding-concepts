# https://leetcode.com/problems/flood-fill/


class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        if not image or not image[0]:
            return image
        startColor = image[sr][sc]
        image[sr][sc] = color
        queue = deque()
        queue.append((sr, sc))
        visited = set()
        visited.add((sr,sc))

        directions = [(-1,0), (0, -1), (1, 0), (0, 1)]
        n, m = len(image), len(image[0])
        while(queue):
            rx, cx = queue.popleft()
            for (ry,cy) in directions:
                newRow, newCol = rx+ry, cx+cy
                if 0 <= newRow < n and 0 <= newCol < m and (newRow, newCol) not in visited and image[newRow][newCol] == startColor:
                    visited.add((newRow, newCol))
                    queue.append((newRow, newCol))
                    image[newRow][newCol] = color
        return image



        