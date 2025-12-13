from typing import List
class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        ans = set()
        self.helper(0, candidates, target, [], ans)
        print(ans)
        return [[7,3]]
    
    def helper(self, i, candidates, target, combinations, ans):
        if i >= len(candidates):
            combinations = []
            return
        if target == 0:
            ans.add(tuple(combinations))
            combinations = []
        if target < 0:
            combinations = []
            return
        self.helper(i+1,candidates, target, combinations, ans)
        combinations.append(candidates[i])
        self.helper(i, candidates, target-candidates[i], combinations, ans)
      
    
def main():
   print(Solution().combinationSum([2,3,6,7], 7))

main()