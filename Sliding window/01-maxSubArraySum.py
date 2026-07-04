from typing import List
class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        start = 0
        visited = set()
        windowSum = 0
        result = 0
        
        for end in range(len(nums)):
            # 1. SHRINK: Remove duplicates OR excess size
            while nums[end] in visited or end - start + 1 > k:
                visited.discard(nums[start])
                windowSum -= nums[start]
                start += 1
            
            # 2. EXPAND: Add current element
            visited.add(nums[end])
            windowSum += nums[end]
            
            # 3. CHECK: Valid window of size k
            if end - start + 1 == k:
                result = max(result, windowSum)
        
        return result

            

print(Solution().maximumSubarraySum([1,5,4,2,9,9,9], 3))