class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort(key = lambda x: x[1])
        count =  0
        merged = []
        for interval in intervals:
            if not merged or merged[-1][1] <= interval[0]:
                merged.append(interval)
            else:
                count += 1
        return count
        
        # [[1,2],[2,3],[1,3], [3,4]]
