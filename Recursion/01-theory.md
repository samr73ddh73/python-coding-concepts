1. Each Recursion call, requires extra space on the stack frame.
2. if we get infinite recursion, the program will run out of memory with stack overflow
3. Generally, iterative functions are more efficient than recursive functions due to overhead of function calls in recursion


Pattern of recursion:

/*
function rec(x):
    if(xxx) //base condition
        return xxx;
    else if (yyy):
        return yyy; //another base condition
    return work + rec(y)
*/

Problems:

class Solution:
    def isPowerOfThree(self, n: int) -> bool:
        if(n == 1):
            return True
        if(n == 0):
            return False
        return self.isPowerOfThree(n/3)


        