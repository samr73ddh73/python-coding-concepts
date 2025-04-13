class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        grouped = {}
        for word in strs:
            sortedWord = ''.join(sorted(word))
            if sortedWord not in grouped:
                grouped[sortedWord] = []
            grouped[sortedWord].append(word)
        return list(grouped.values())
        
A naive solution would be to sort each string and group them using a hash map. This would be an O(m * nlogn) solution. Though this solution is acceptable, can you think of a better way without sorting the strings?