class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        nonDuplicateIndex = 0
        unique = set()
        for i in range(len(nums)):
            if nums[i] in unique:
                nonDuplicateIndex = min(nonDuplicateIndex, i)
            else:
                unique.add(nums[i])
                self.swap(nums, i, nonDuplicateIndex)
                nonDuplicateIndex += 1
                
        return len(unique)
        
    def swap(self, nums, i, j):
        temp = nums[i]
        nums[i] = nums[j]
        nums[j] = temp