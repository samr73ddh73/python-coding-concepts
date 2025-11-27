def flood_fill(sr: int, sc: int, replacement: int, image: list[list[int]]) -> list[list[int]]:
    # WRITE YOUR BRILLIANT CODE HERE
    queue = [(sr,sc)]
    visited = set()
    visited.add((sr,sc))
    initialColor = image[sr][sc]
    image[sr][sc] = replacement
    dir = [(0,1), (1,0), (-1,0), (0,-1)]
    n, m = len(image), len(image[0])
    while(queue):
        r,c = queue.pop()
        for dr, dc in dir:
            newR, newC = dr+r, dc+c
            if 0<=newR<n and 0<=newC<m and (newR,newC) not in visited and image[newR][newC] == initialColor:
                image[newR][newC] = replacement
                visited.add((newR, newC))
                queue.append((newR, newC))  
    return image

if __name__ == "__main__":
    r = int(input())
    c = int(input())
    replacement = int(input())
    image = [[int(x) for x in input().split()] for _ in range(int(input()))]
    res = flood_fill(r, c, replacement, image)
    for row in res:
        print(" ".join(map(str, row)))
