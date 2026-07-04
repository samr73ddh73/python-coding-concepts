class Solution:
    def getAllMax(self, s, startIndex):
        if len(s[startIndex::]) == 0:
            return []
        maxEl = max(s[startIndex::])
        if maxEl == s[startIndex]:
            return []
        res = []
        for i in range(startIndex, len(s)):
            if s[i] == maxEl:
                res.append(i)
        return res
    
    def swap(self, slist, i, j):
        temp = slist[i]
        slist[i] = slist[j]
        slist[j] = temp
    def findMaximumNum(self, s, k):
        slist = list(s)
        maxNum = float('-inf')
        maxNum = self._findMaximumNum(slist, 0, k, maxNum)
        return str(maxNum)
        
    def _findMaximumNum(self, s, i, k, maxNum):
        print(s)
        if k <= 0 or i >= len(s):
            return int(''.join(s))
        choices = self.getAllMax(s, i)
        print('choices', choices)
        if len(choices) == 0:
            maxNum = max(self._findMaximumNum(s,i+1,k, maxNum), maxNum)
        for choice in choices:
            self.swap(s, i, choice)
            maxNum = max(self._findMaximumNum(s,i+1,k-1, maxNum), maxNum)
            self.swap(s, choice, i)
        
        return maxNum
        
        
def main():
    print(Solution().findMaximumNum('42431636', 3))

main()