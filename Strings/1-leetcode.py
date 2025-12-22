class Solution:
    def minDeletions(self, s: str, queries: List[List[int]]) -> List[int]:
        ans = []
        # AABBBAAABABBA
        def createPrefixArray(slicedS):
            prefixArray = []
            while(i< len(slicedS)):
                while (i< len(slicedS) and slicedS[i] != startChar):
                    startChar = slicedS[i]
                    i+=1
                    prefixArray.append(delete)
                if i < len(slicedS):
                    delete += 1
                    i += 1
                prefixArray.append(delete)
            print(prefixArray)
            return prefixArray
        for q in queries:
            if q[0] == 1:
                l = list(s)
                l[q[1]] = 'B' if l[q[1]] == 'A' else 'A'
                s = ''.join(l)
                prefixArray = createPrefixArray(s)
            else:
                delete = 0
                slicedS = s[q[1]:q[2]+1]
                startChar = slicedS[0]
                i = 1
                while(i< len(slicedS)):
                    while (i< len(slicedS) and slicedS[i] != startChar):
                        startChar = slicedS[i]
                        i+=1
                    if i < len(slicedS):
                        delete += 1
                        i += 1
                ans.append(delete)
        return ans