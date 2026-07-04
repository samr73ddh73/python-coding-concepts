#When there is unbounded case. 

# https://leetcode.com/problems/minimum-speed-to-arrive-on-time/description/

from typing import List
import math
class Solution:
    def minSpeedOnTime(self, dist: List[int], hour: float) -> int:
        l, r = 1, 10**7
        time = 0
        minSpeed = float('inf')
        minTime = float('inf')
        while l <= r:
            speed = (l+r)//2
            # print("speed", speed)
            # if speed
            time = 0
            for i in range(len(dist)-1):
                time += math.ceil(dist[i]/speed)
            time += dist[len(dist)-1]/speed
            if time <= hour:
                minSpeed = min(speed, minSpeed)
                minTime = time
                r = speed-1
            else:
                l = speed+1
        return -1 if minTime > hour else minSpeed