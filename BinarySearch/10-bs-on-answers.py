from typing import List
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        def canEatBananas(k, hr):
            for pile in piles:
                hr = hr - math.ceil(pile/k)
            if hr >= 0:
                return True
            return False
        
        l,r = 1, max(piles)
        minK = float('inf')
        while l<=r :
            mid = (l+r)//2
            if canEatBananas(mid,h):
                minK = mid
                r = mid-1
            else:
                l = mid + 1
        return minK

        