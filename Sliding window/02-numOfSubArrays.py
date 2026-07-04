from typing import List
class Solution:
    def numOfSubarrays(self, nums: List[int], k: int, threshold: int) -> int:
        numOfSubarrays = 0
        start, end = 0, 0
        windowSum = 0

        for end in range(len(nums)):
            while end-start+1 > k:
                windowSum -= nums[start]
                start += 1
            windowSum += nums[end]

            if end - start + 1 == k:
                avg = windowSum/k
                if avg >= threshold:
                    numOfSubarrays += 1
            
        return numOfSubarrays

print(Solution().numOfSubarrays([11,13,17,23,29,31,7,5,2,3], 3, 5))