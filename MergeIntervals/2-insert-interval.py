class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        if len(intervals) == 0:
            intervals.append(newInterval)
            return intervals
        merged = []
        added = False
        for i in range(len(intervals)):
            interval = intervals[i]
            if newInterval[0] <= interval[0] and not added:
                if not merged or merged[-1][1] < newInterval[0]:
                    merged.append(newInterval)
                    added = True
                else:
                    merged[-1][1] = max(merged[-1][1], newInterval[1])
                    added = True
            if not merged or merged[-1][1] < interval[0]:
                merged.append(interval)
            else:
                merged[-1][1] = max(merged[-1][1], interval[1])
        
        if added == False:
            if  merged[-1][1] < newInterval[0]:
                    merged.append(newInterval)
                    added = True
            else:
                merged[-1][1] = max(merged[-1][1], newInterval[1])
                added = True

        return merged
