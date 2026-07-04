from typing import List
from collections import defaultdict
class Solution:
    def findRepeatedDnaSequences(self, s: str) -> List[str]:
        hashMap = defaultdict(int)
        start, count = 0,0
        tempStr = []
        for end in range(len(s)):
            while end-start+1 > 10:
                start += 1
            tempStr.append(s[end])
            if end-start+1 == 10:
                str = ''.join(tempStr[start:])
                if str in hashMap and hashMap[str] == 1:
                    count += 1
                hashMap[str] += 1
        return count

print(Solution().findRepeatedDnaSequences('AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT'))