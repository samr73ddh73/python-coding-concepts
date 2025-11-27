"""
================================================================================
PATTERN: Generate Binary Strings Without Consecutive 1s
================================================================================

PROBLEM:
Given an integer n, return all binary strings of length n that do not contain
consecutive 1s. Return result in lexicographically increasing order.

CONSTRAINT: Cannot have "11" as substring

Examples:
n=2: ["00", "01", "10"]  (exclude "11")
n=3: ["000", "001", "010", "100", "101"]  (exclude "011", "110", "111")

APPROACH: Backtracking/Recursion
- At each position, try adding '0' or '1'
- Only add '1' if previous character is not '1'
- This ensures no consecutive 1s

TIME COMPLEXITY: O(2^n) - in worst case, explore all possibilities
SPACE COMPLEXITY: O(n) - recursion depth
"""

# ============================================================================
# SOLUTION 1: Your Approach (String Concatenation) - Clean Version
# ============================================================================
class Solution:
    def generateBinaryStrings(self, n):
        """
        TIME: O(2^n) - each position has up to 2 choices
        SPACE: O(n) - recursion depth
        """
        result = []
        self.helper(n, '', result)
        return result

    def helper(self, n, current, result):
        # Base case: reached length n
        if n == 0:
            result.append(current)
            return

        # Always can add '0'
        self.helper(n - 1, current + '0', result)

        # Can add '1' only if last char is not '1'
        if not current or current[-1] != '1':
            self.helper(n - 1, current + '1', result)


# ============================================================================
# SOLUTION 2: List-Based (More Efficient) ✓ RECOMMENDED
# ============================================================================
class SolutionOptimized:
    def generateBinaryStrings(self, n):
        """
        Use list instead of string concatenation
        More efficient for large n (avoid creating new strings each time)

        TIME: O(2^n)
        SPACE: O(n) recursion + O(n) for path list
        """
        result = []
        self.backtrack(n, [], result)
        return result

    def backtrack(self, n, path, result):
        # Base case: path has length n
        if len(path) == n:
            result.append(''.join(path))
            return

        # Add '0'
        path.append('0')
        self.backtrack(n, path, result)
        path.pop()  # Backtrack

        # Add '1' only if last is not '1'
        if not path or path[-1] != '1':
            path.append('1')
            self.backtrack(n, path, result)
            path.pop()  # Backtrack


