[Pattern and questions for cycle sort](https://leetcode.com/discuss/post/2958275/cyclic-sort-important-pattern-by-sourin_-e9tr/)


1. Given that the elements in a given sequence are in a range, say [1, n], we can apply Cyclic sort and sort our array in linear time.

2. Since if arrays are in a given range within len(arr), we would always know the right index of an element. We will swap until a given element reaches it's correct destination

3. Remember: there will be cases which we need to skip to avoid cycles. 

4. Template:

```
class Solution:
    def findErrorNums(self, nums: List[int]) -> List[int]:
        def swap(i, j):
            t = nums[i]
            nums[i] = nums[j]
            nums[j] = t

        n, i = len(nums), 0
        while(i < n):
            correctIndx = nums[i]-1
            if nums[i] != nums[correctIndx]:   # this condition will change based on the question. (it is to avoid a cycle or duplicate values.)
                swap(i, correctIndx)
            else:
                i += 1
        for i in range(n):
            if i != nums[i]-1:
                return [nums[i], i+1]
        return []
```

