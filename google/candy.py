import heapq
from typing import List
class Solution:
    def candy(self, ratings: List[int]) -> int:
        pq = []
        for i in range(len(ratings)):
            heapq.heappush(pq, (ratings[i],i))
        print(pq)
        candy = [1 for _ in range(len(ratings))]
        dirs = [-1, 1]
        while(pq):
            minRating, index = heapq.heappop(pq)
            maxCandy = 0
            for d in dirs:
                dx = index + d
                if dx >= 0 and dx <len(ratings) and ratings[index] > ratings[dx]:
                    maxCandy = max(maxCandy, candy[dx])
            candy[index] = maxCandy + 1
        return sum(candy)

def main():
    sol = Solution().candy([1,2,2])
    print(sol)

main()
                

            